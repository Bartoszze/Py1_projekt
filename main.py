import cv2
import numpy as np

try:
    refColor = cv2.imread('./media/ref.jpg')
    cutoutColor = cv2.imread('./media/cutout.jpg')

    if refColor is None or cutoutColor is None:
        exit()

    refGray = cv2.cvtColor(refColor, cv2.COLOR_BGR2GRAY)
    cutoutGray = cv2.cvtColor(cutoutColor, cv2.COLOR_BGR2GRAY)

except cv2.error as err:
    exit()

# SIFT
sift = cv2.SIFT_create()

keyPointsRef, desRef = sift.detectAndCompute(refGray, None)
keyPointsCutout, desCutout = sift.detectAndCompute(cutoutGray, None)

if desRef is None or desCutout is None or len(keyPointsRef) == 0 or len(keyPointsCutout) == 0:
    exit()

# Matching feature
matcher = cv2.BFMatcher(cv2.NORM_L2)

# knnMatches
knnMatches = matcher.knnMatch(desCutout, desRef, k=2)

good = []
rThresh = 0.75

for matchPair in knnMatches:
    if len(matchPair) == 2:
        m, n = matchPair  # m to pierwsze najlepsze dopasowanie a n to drugie
        if m.distance < rThresh * n.distance:  # Jeśli m jest znacznie lepsze niż n (o 25%) to je  akceptujemy
            good.append(m)


# RANSAC
minMatchCount = 10

if len(good) > minMatchCount:
    # Współrzędne punktów z 'cutout' (obraz "query")
    srcPts = np.float32([keyPointsCutout[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    # Współrzędne punktów z 'ref' (obraz "train")
    dstPts = np.float32([keyPointsRef[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # homografia RANSAC
    M, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5.0)

    if M is None:
        print("Nie udało się znaleźć homografii.")
        exit()

    # Maska inliers
    matchesMask = mask.ravel().tolist()

    # Pobranie wymiarow obrazu  aby narysować ramkę
    h, w = cutoutGray.shape
    #  rogi obrazu 'cutout'
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)

    # Przekształcenie rogow wycinka do perspektywy obrazu ref używając homografii M
    dst = cv2.perspectiveTransform(pts, M)
# ramka
    refColorWithBox = cv2.polylines(refColor.copy(), [np.int32(dst)], True, (0, 255, 255), 3, cv2.LINE_AA)
    draw_params = dict(matchColor=(0, 255, 0),  # Zielone linie dla "inliers"
                       singlePointColor=None,
                       matchesMask=matchesMask,  # dopasowania z maski RANSAC
                       flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # finalny obraz z dopasowaniami (tylko inliers)
    imgMatches = cv2.drawMatches(cutoutColor, keyPointsCutout, refColorWithBox, keyPointsRef, good, None, **draw_params)


    cv2.imshow('Wynik dopasowania', imgMatches)
    cv2.waitKey(0)

else:
    exit()

cv2.destroyAllWindows()
