#ifndef _SCUKE_UTILS_H
#define _SCUKE_UTILS_H

highp vec3 get_world_position(vec2 uv, float z) {
    highp vec4 pos_clip = vec4(uv, z, 1.0) * 2.0 - 1.0;
    highp vec4 pos_world = inverse(PROJ*WORLDVIEW) * pos_clip;
    return pos_world.xyz / pos_world.w;
}

float get_linear_depth(float z, float n, float f)
{
    // scale z to [0,1]
    z = 2.0 * z - 1.0;
    return (2.0 * n) / (f + n - z * (f - n));
}

bool float_equal(float a, float b) {
    return abs(a - b) < 0.001;
}

bool float_less_equal(float a, float b) {
    return a < b + 0.001;
}

#endif