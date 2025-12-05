# -*- encoding: utf-8 -*-
import math

from common.utils.mcmath import Quaternion as Quat
from common.utils.mcmath import Vector3 as Vec3
from common.utils.mcmath import Matrix as Matx
from math import floor


class MathUtils(object):
	@staticmethod
	def Clamp(value, minValue, maxValue):
		# type: (float, float, float) -> float
		return min(max(value, minValue), maxValue)
	
	@staticmethod
	def Lerp(start, end, t):
		# type: (float, float, float) -> float
		return start + (end - start) * t

	@staticmethod
	def TupleAdd(v1, v2):
		# type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
		return tuple((a + b) for a, b in zip(v1, v2))

	@staticmethod
	def TupleMin(v1, v2):
		# type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
		return tuple(min(a, b) for a, b in zip(v1, v2))

	@staticmethod
	def TupleMax(v1, v2):
		# type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
		return tuple(max(a, b) for a, b in zip(v1, v2))

	@staticmethod
	def TupleSub(v1, v2):
		# type: (Tuple[float,...], Tuple[float,...]) -> Tuple[float,...]
		return tuple((a - b) for a, b in zip(v1, v2))

	@staticmethod
	def TupleAddMul(v1, v2, k):
		# type: (Tuple[float,...], Tuple[float,...], float) -> Tuple[float,...]
		return tuple((a + b * k) for a, b in zip(v1, v2))

	@staticmethod
	def TupleMul(v, k):
		# type: (Tuple[float,...], float) -> Tuple[float,...]
		return tuple((a * k) for a in v)

	@staticmethod
	def TupleLength(v, sqrt=True):
		# type: (Tuple[float,...], float) -> float
		length = 0
		for a in v:
			length += a * a
		if not sqrt:
			return length
		return math.sqrt(length)

	@staticmethod
	def TupleFloor2Int(v):
		# type: (Tuple[float,float,float]) -> Tuple[int,int,int]
		return tuple(map(int, map(floor, v)))

	@staticmethod
	def TupleRound(v, p):
		# type: (Tuple[float,float,float]) -> Tuple[int,int,int]
		return tuple(round(a, p) for a in v)

	@staticmethod
	def LookDirection(direction=Vec3.Forward(), up=Vec3.Up()):
		# type: (Vector3, Vector3) -> Quaternion
		return Quat.LookDirection(-direction, up)

	@staticmethod
	def InverseRot(rot):
		return Quat.Inverse(rot)

	@staticmethod
	def RotByFace(pos, rot):
		ret = pos
		if rot < 0:
			rot += 360
		if rot == 90:
			ret = (-pos[2], pos[1], pos[0])
		elif rot == 180:
			ret = (-pos[0], pos[1], -pos[2])
		elif rot == 270:
			ret = (pos[2], pos[1], -pos[0])
		return ret

	@staticmethod
	def _CubicSplineLerp(points, i, t):
		n = len(points) - 1
		p0 = points[max(i - 1, 0)]
		p1 = points[i]
		p2 = points[min(i + 1, n)]
		p3 = points[min(i + 2, n)]

		t2 = t * t
		t3 = t2 * t

		a = (0.5 * (p2[0] - p0[0]), 0.5 * (p2[1] - p0[1]), 0.5 * (p2[2] - p0[2]))
		b = (0.5 * (p3[0] - p1[0]), 0.5 * (p3[1] - p1[1]), 0.5 * (p3[2] - p1[2]))

		result = [
			(2 * t3 - 3 * t2 + 1) * p1[j] +
			(t3 - 2 * t2 + t) * a[j] +
			(-2 * t3 + 3 * t2) * p2[j] +
			(t3 - t2) * b[j]
			for j in range(3)
		]
		return tuple(result)

	@staticmethod
	def CubicSplineInterpolation(points, p, total=0.0, splinesDis=None):
		n = len(points) - 1
		t = p * n
		i = int(t)
		t = t - i
		if total > 0 and splinesDis is not None:
			i = 0
			targetDis = p * total
			curDis = 0.0
			t = 0.0
			while i < len(splinesDis):
				temp = curDis + splinesDis[i]
				if temp > targetDis:
					t = (targetDis - curDis)/splinesDis[i]
					i -= 1
					break
				curDis = temp
				i += 1
		if i >= n:
			i = n - 1
			t = 1
		return MathUtils._CubicSplineLerp(points, i, t)


	@staticmethod
	def CubicSplinePrepare(points, disFunc):
		total = 0.0
		splinesDis = [0.0]
		i = 0
		n = len(points)-1
		while i < n:
			dis = disFunc(points, i, i+1)
			splinesDis.append(dis)
			total += dis
			i += 1
		return total, splinesDis

	@staticmethod
	def CubicSplineDis(points, ia, ib):
		p0 = points[ia]
		dis = 0.0
		for i in range(0, 20):
			t = float(i+1.0)/20.0
			p = MathUtils._CubicSplineLerp(points, ia, t)
			dis += MathUtils.TupleLength(MathUtils.TupleSub(p, p0))
			p0 = p
		return dis

	@staticmethod
	def CubicPosTupleDis(points, ia, ib):
		a = points[ia]
		b = points[ib]
		return MathUtils.TupleLength(MathUtils.TupleSub(a, b))

	@staticmethod
	def CubicRotTupleDis(points, ia, ib):
		a = points[ia]
		b = points[ib]
		q1 = Quaternion.Euler(a[0], a[1], a[2])
		q2 = Quaternion.Euler(b[0], b[1], b[2])
		dot_product = Quaternion.Dot(q1, q2)
		return math.acos(2 * dot_product ** 2 - 1)


	@staticmethod
	def WorldPos2CameraPos(pos, camPos, camRot, camAnchor=(0,0,0)):
		rotI = Quaternion.Inverse(Quaternion.Euler(camRot[0], 180 - camRot[1], camRot[2]))  # right-hand rotation
		pos2cam = Vector3(pos) - Vector3(camAnchor) - Vector3(camPos)
		cPos = rotI * pos2cam
		return cPos.ToTuple()

	@staticmethod
	def WorldPos2ScreenPos(pos, camPos, camRot, camFov, screenSize, camAnchor=(0,0,0)):
		near = 0.025
		far = 2500.0
		hfWidth = screenSize[0] / 2.0
		hfHeight = screenSize[1] / 2.0
		aspect = hfWidth / hfHeight
		# camera space
		cPos = MathUtils.WorldPos2CameraPos(pos, camPos, camRot, camAnchor)
		pMat = Matrix.Create([[cPos[0], cPos[1], cPos[2], 1.0]]).Transpose()
		# view space
		vMat = Matrix.Create((
			(hfWidth, 0.0, 0.0, hfWidth),
			(0.0, hfHeight, 0.0, hfHeight),
			(0.0, 0.0, 1.0, 0.0),
			(0.0, 0.0, 0.0, 1.0)
		))
		sV = math.tan(math.radians(camFov * 0.5)) * near
		l = sV * aspect
		r = -l
		t = -sV
		b = -t
		projMat = Matrix.Create((
			(2 * near / (r - l), 0, 0, 0),
			(0, 2 * near / (t - b), 0, 0),
			(0, 0, (far + near) / (far - near), 2 * far * near / (far - near)),
			(0, 0, 1, 0)
		))
		screenPos = vMat * projMat * pMat
		x = screenPos[0, 0]
		y = screenPos[1, 0]
		z = screenPos[2, 0]
		w = screenPos[3, 0]
		ret = (x / w, y / w, z / w, cPos[2])
		return ret


class Vector3(Vec3):
	pass


class Quaternion(Quat):
	pass

class Matrix(Matx):
	pass

Inf = 2147483647
"""整型最大值"""

