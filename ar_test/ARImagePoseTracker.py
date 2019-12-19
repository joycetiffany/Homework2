import cv2
import glob
import numpy as np
import CalibrationHelpers as calib

# ------------------------ Helper functions ------------------------

# take in a set of 3d points and the intrinsic matrix
# rotation matrix(R) and translation vector(T) of a camera
# return the 2d projection of the 3d points onto the camera defined
# by the input parameters
def ProjectPoints(points3d, new_intrinsics, R, T):
    extrinsic_params = np.column_stack((R, T))
    points3d_aug = np.column_stack((points3d, np.ones(len(points3d))))
    points2d_aug = np.transpose(
        new_intrinsics @ extrinsic_params @ points3d_aug.T
    )
    points2d = np.transpose(points2d_aug[:, :-1].T / points2d_aug[:, -1])
    return points2d


# This function will render a cube on an image whose camera is defined
# by the input intrinsics matrix, rotation matrix(R), and translation vector(T)
def renderCube(img_in, new_intrinsics, R, T):
    # Setup output image
    img = np.copy(img_in)

    # We can define a 10cm cube by 4 sets of 3d points
    # these points are in the reference coordinate frame
    scale = 0.1
    face1 = np.array([[0, 0, 0], [0, 0, scale], [0, scale, scale], [0, scale, 0]],
                     np.float32)
    face2 = np.array([[0, 0, 0], [0, scale, 0], [scale, scale, 0], [scale, 0, 0]],
                     np.float32)
    face3 = np.array([[0, 0, scale], [0, scale, scale], [scale, scale, scale],
                      [scale, 0, scale]], np.float32)
    face4 = np.array([[scale, 0, 0], [scale, 0, scale], [scale, scale, scale],
                      [scale, scale, 0]], np.float32)
    # using the function you write above we will get the 2d projected
    # position of these points
    face1_proj = ProjectPoints(face1, new_intrinsics, R, T)
    # this function simply draws a line connecting the 4 points
    img = cv2.polylines(img, [np.int32(face1_proj)], True,
                        tuple([255, 0, 0]), 3, cv2.LINE_AA)
    # repeat for the remaining faces
    face2_proj = ProjectPoints(face2, new_intrinsics, R, T)
    img = cv2.polylines(img, [np.int32(face2_proj)], True,
                        tuple([0, 255, 0]), 3, cv2.LINE_AA)

    face3_proj = ProjectPoints(face3, new_intrinsics, R, T)
    img = cv2.polylines(img, [np.int32(face3_proj)], True,
                        tuple([0, 0, 255]), 3, cv2.LINE_AA)

    face4_proj = ProjectPoints(face4, new_intrinsics, R, T)
    img = cv2.polylines(img, [np.int32(face4_proj)], True,
                        tuple([125, 125, 0]), 3, cv2.LINE_AA)
    # print("cube rendered")
    return img


# This function takes in an intrinsics matrix, and two sets of 2d points
# if a pose can be computed it returns true along with a rotation and
# translation between the sets of points.
# returns false if a good pose estimate cannot be found
def ComputePoseFromHomography(new_intrinsics, referencePoints, imagePoints):
    # compute homography using RANSAC, this allows us to compute
    # the homography even when some matches are incorrect
    homography, mask = cv2.findHomography(referencePoints, imagePoints,
                                          cv2.RANSAC, 5.0)
    # check that enough matches are correct for a reasonable estimate
    # correct matches are typically called inliers
    MIN_INLIERS = 30
    if(sum(mask) > MIN_INLIERS):
        # given that we have a good estimate
        # decompose the homography into Rotation and translation
        # you are not required to know how to do this for this class
        # but if you are interested please refer to:
        # https://docs.opencv.org/master/d9/dab/tutorial_homography.html
        RT = np.matmul(np.linalg.inv(new_intrinsics), homography)
        norm = np.sqrt(np.linalg.norm(RT[:, 0]) * np.linalg.norm(RT[:, 1]))
        RT = -1 * RT / norm
        c1 = RT[:, 0]
        c2 = RT[:, 1]
        c3 = np.cross(c1, c2)
        T = RT[:, 2]
        R = np.vstack((c1, c2, c3)).T
        W, U, Vt = cv2.SVDecomp(R)
        R = np.matmul(U, Vt)
        return True, R, T
    # return false if we could not compute a good estimate
    return False, None, None


def calc_rotation_and_translation(img,
                                  new_intrinsics,
                                  feature_detector, matcher,
                                  reference_keypoints, reference_descriptors):
    # detect features in the current image
    current_keypoints, current_descriptors = \
        feature_detector.detectAndCompute(img, None)
    # match the features from the reference image to the current image
    if (len(current_keypoints) == 0):
        print("[ERROR] Feature detection failed for file " + fname)
        return False, None, None
    # matches returns a vector where for each element there is a
    # query index matched with a train index.
    # query will refer to a feature in the reference image
    # train will refer to a feature in the current image
    matches = matcher.match(reference_descriptors, current_descriptors)
    # set up reference points and image points
    # here we get the 2d position of all features in the reference image
    referencePoints = np.float32([reference_keypoints[m.queryIdx].pt
                                  for m in matches])
    # convert positions from pixels to meters
    SCALE = 0.1  # this is the scale of our reference image: 0.1m x 0.1m
    referencePoints = SCALE * referencePoints / RES

    imagePoints = np.float32([current_keypoints[m.trainIdx].pt
                              for m in matches])
    # compute homography
    ret, R, T = ComputePoseFromHomography(new_intrinsics, referencePoints,
                                          imagePoints)
    return ret, R, T




# ------------------------ Load data ------------------------


# Load the reference image that we will try to detect in the webcam
reference = cv2.imread('./ARTrackerImage.jpg', 0)
RES = 480
reference = cv2.resize(reference, (RES, RES))

# create the feature detector. This will be used to find and describe locations
# in the image that we can reliably detect in multiple images
feature_detector = cv2.BRISK_create(octaves=5)
# compute the features in the reference image
reference_keypoints, reference_descriptors = \
    feature_detector.detectAndCompute(reference, None)

# create the matcher that is used to compare feature similarity
# Brisk descriptors are binary descriptors (a vector of zeros and 1s)
# Thus hamming distance is a good measure of similarity
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Load the camera calibration matrix
intrinsics, distortion, new_intrinsics, roi = \
    calib.LoadCalibrationData('calibration_data')

# --------- Step 3: Compute pose of camera w.r.t. reference image ---------

# cd | bottle | keyboard | intel
obj = "cd" + "/"
# obj = "intel" + "/"
ref_imgs = glob.glob(obj + '*.jpeg')
R_nr = []
T_nr = []
img_ls = []
for fname in ref_imgs:
    # read the image
    img = cv2.imread(fname)
    # resize image by 0.25
    img_resize_scale = 0.25
    img = cv2.resize(img, (0, 0), fx=img_resize_scale, fy=img_resize_scale)
    # undistort the image using the loaded calibration
    img = cv2.undistort(img, intrinsics, distortion, None, new_intrinsics)
    # apply region of interest cropping
    x, y, w, h = roi
    img = img[y:y + h, x:x + w]
    img_ls.append(img)
    # compute rotation and translation
    ret, R, T = calc_rotation_and_translation(img,
                                              new_intrinsics,
                                              feature_detector, matcher,
                                              reference_keypoints, reference_descriptors)
    R_nr.append(R)
    T_nr.append(T)
    # render frame
    render_frame = img
    if(ret):
        # compute the projection and render the cube
        render_frame = renderCube(img, new_intrinsics, R, T)

    # display the current image frame
    cv2.imshow('frame', render_frame)

    k = cv2.waitKey(0)
    if k == 27 or k == 113:  # 27, 113 are ascii for escape and q respectively
        # exit
        break

# ----------------- Step 4: Compute relative pose between cameras -----------------

# R_n1[i] = R_nr[i] @ R_nr[0].T
# T_n1[i] = T_nr[i] - R_nr[i] @ R_nr[0].T @ T_nr[0]

R_n1 = []
T_n1 = []
for R_ir, T_ir in zip(R_nr, T_nr):
    R_n1.append(R_ir @ R_nr[0].T)
    T_n1.append(T_ir - R_ir @ R_nr[0].T @ T_nr[0])


# print(M)
W, U, Vt = cv2.SVDecomp(M)
depths = Vt[-1, :] / Vt[-1, -1]

# ---- Step 9: Compute 3D position of tracked features in image ----

depths_mat = np.tile(depths[:-1], (3,1))
x_1_ls = np.array([tuple_ls[0][0] for tuple_ls in filtered_feature_map.values()])
feature_pos = np.multiply(x_1_ls, depths_mat.T)

# ----- Step 10: Visualize sparse point cloud -----

import open3d as o3d
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(feature_pos)
o3d.visualization.draw_geometries([pcd])

