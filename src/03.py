import cv2

float_img = cv2.imread('data/ALOS2237752900-181018/IMG-HH-ALOS2237752900-181018-UBSR2.1GUD.tif_cropped.tif', cv2.IMREAD_GRAYSCALE)
ref_img = cv2.imread('data/asnaro/20181224060959386_AS1.png', cv2.IMREAD_GRAYSCALE)

akaze = cv2.AKAZE_create()
float_kp, float_des = akaze.detectAndCompute(float_img, None)
ref_kp, ref_des = akaze.detectAndCompute(ref_img, None)
bf = cv2.BFMatcher()
matches = bf.knnMatch(float_des, ref_des, k=2)
good_matches = []
for m, n in matches:
    if m.distance < 0.95 * n.distance:
        good_matches.append([m])

matches_img = cv2.drawMatchesKnn(
    float_img,
    float_kp,
    ref_img,
    ref_kp,
    good_matches,
    None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imwrite('matches.png', matches_img)
