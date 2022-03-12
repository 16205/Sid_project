import calibration
import image_processing

ret, mtx, dist, rvecs, tvecs = calibration.calibration()

print(ret)
print("################################")
print(mtx)
print("################################")
print(dist)
print("################################")
print(rvecs)
print("################################")
print(tvecs)