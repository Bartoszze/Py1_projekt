import cv2
import numpy as np
import base64

class ImageMatcher:
    def process(self, cutout_bytes, ref_bytes):
        try:
            nparr_cutout = np.frombuffer(cutout_bytes, np.uint8)
            nparr_ref = np.frombuffer(ref_bytes, np.uint8)

            cutout_color = cv2.imdecode(nparr_cutout, cv2.IMREAD_COLOR)
            ref_color = cv2.imdecode(nparr_ref, cv2.IMREAD_COLOR)


            if ref_color is None or cutout_color is None:
                return {"err": "Failed to decode images from memory"}

            ref_gray = cv2.cvtColor(ref_color, cv2.COLOR_BGR2GRAY)
            cutout_gray = cv2.cvtColor(cutout_color, cv2.COLOR_BGR2GRAY)

            # CLAHE (Poprawa kontrastu - przydatne przy różnych oświetleniach)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            ref_gray = clahe.apply(ref_gray)
            cutout_gray = clahe.apply(cutout_gray)

            # SIFT
            sift = cv2.SIFT_create()
            kp_ref, des_ref = sift.detectAndCompute(ref_gray, None)
            kp_cutout, des_cutout = sift.detectAndCompute(cutout_gray, None)

            if des_ref is None or des_cutout is None or len(kp_ref) == 0 or len(kp_cutout) == 0:
                return {"matches": 0, "err": "No key points detected"}

            matcher = cv2.BFMatcher(cv2.NORM_L2)
            knn_matches = matcher.knnMatch(des_cutout, des_ref, k=2)

            good = []
            for match_pair in knn_matches:
                if len(match_pair) == 2:
                    m, n = match_pair
                    if m.distance < 0.75 * n.distance:
                        good.append(m)

            min_match_count = 10
            
            if len(good) >= min_match_count:
                src_pts = np.float32([kp_cutout[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_ref[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
                if M is None:
                     return {"matches": len(good), "err": "Failed to find homography"}
                
                matches_mask = mask.ravel().tolist()

                h, w = cutout_gray.shape
                pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
                
                try:
                    dst = cv2.perspectiveTransform(pts, M)
                    ref_color_with_box = cv2.polylines(ref_color.copy(), [np.int32(dst)], True, (0, 255, 255), 3, cv2.LINE_AA)
                except Exception:
                    ref_color_with_box = ref_color

                draw_params = dict(matchColor=(0, 255, 0),
                                   singlePointColor=None,
                                   matchesMask=matches_mask,
                                   flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

                img_matches = cv2.drawMatches(cutout_color, kp_cutout, ref_color_with_box, kp_ref, good, None, **draw_params)

                success, buffer = cv2.imencode('.png', img_matches)
                if not success:
                    return {"err": "Failed to encode output image"}
                
                img_base64 = base64.b64encode(buffer).decode('utf-8')

                return {
                    "success": True,
                    "matches": len(good), # Zwracamy liczbę dopasowań
                    "result_base64": img_base64
                }
            else:
                return {
                    "success": False, 
                    "matches": len(good), 
                    "err": f"Insufficient matches: {len(good)}/{min_match_count}"
                }

        except cv2.error as err:
            return {"err": f"OpenCV error: {str(err)}"}
        except Exception as e:
            return {"err": f"Processing error: {str(e)}"}