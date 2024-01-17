import pytest

import arm_demo

from panda3d.core import LVector3f
import math

env = arm_demo.Env(debug=False)
env.dx = 0
env.dy = 0
env.dz = 0


@pytest.mark.arm_demo
def test_get_len_vecThreeFour_five():
    vec = [3, 4]
    length = env.get_len(vec)
    
    assert length == 5


@pytest.mark.arm_demo
def test_get_len_vecOneTwoFourTen_eleven():
    vec = [1, 2, 4, 10]
    length = env.get_len(vec)
    
    assert length == 11


@pytest.mark.arm_demo
def test_rotate_threeFourPI_roughlyNegativeThreeNegativeFour():
    vec = [3, 4, 0]
    angle = math.pi
    qx, qy = env.rotate(vec, angle)
    
    assert -3 + 0.01 > qx > -3 - 0.01
    assert -4 + 0.01 > qy > -4 - 0.01


@pytest.mark.arm_demo
def test_rotate_threeFourHalfPI_roughlyNegativeFourThree():
    vec = [3, 4, 1]
    angle = 0.5 * math.pi
    qx, qy = env.rotate(vec, angle)
    
    assert -4 + 0.01 > qx > -4 - 0.01
    assert 3 + 0.01 > qy > 3 - 0.01


@pytest.mark.arm_demo
def test_vec_to_world_oneOneOneTwoTwo_zeroNegativeFourTwoTimesSqrtTwo():
    vec = [1, 1, 1]
    bas = [2, 2]
    ref = LVector3f(0, 0, 0)
    tar = env.vec_to_world(vec, bas, ref)
    
    assert 0 + 0.01 > tar[0] > 0 - 0.01
    assert 4 + 0.01 > tar[1] > -4 - 0.01
    assert 2 * math.sqrt(2) + 0.01 > tar[2] > 2 * math.sqrt(2) - 0.01


@pytest.mark.arm_demo
def test_rst():
    env.rst()
    
    assert env.dx == env.dy == env.dz == 0


@pytest.mark.arm_demo
def test_xp():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.xp()
    
    assert env.dx == x + 10
    assert env.dy == y
    assert env.dz == z


@pytest.mark.arm_demo
def test_xn():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.xn()
    
    assert env.dx == x - 10
    assert env.dy == y
    assert env.dz == z


@pytest.mark.arm_demo
def test_yp():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.yp()
    
    assert env.dx == x
    assert env.dy == y + 10
    assert env.dz == z


@pytest.mark.arm_demo
def test_yn():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.yn()
    
    assert env.dx == x
    assert env.dy == y - 10
    assert env.dz == z


@pytest.mark.arm_demo
def test_zp():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.zp()
    
    assert env.dx == x
    assert env.dy == y
    assert env.dz == z + 10


@pytest.mark.arm_demo
def test_zn():
    x = env.dx
    y = env.dy
    z = env.dz
    
    env.zn()
    
    assert env.dx == x
    assert env.dy == y
    assert env.dz == z - 10
