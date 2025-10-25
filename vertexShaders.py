



vertex_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main()
{
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(inPosition, 1.0);

    fragPosition = modelMatrix * vec4(inPosition, 1.0);

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


# NUEVO SHADER 1: Twist Shader - Torsión dinámica
twist_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    // Calcular el ángulo de torsión basado en la altura (Y) y el tiempo
    float twistAmount = value * 3.0; // Controla la intensidad de la torsión
    float angle = pos.y * twistAmount + time * 2.0;
    
    // Aplicar rotación en el plano XZ
    float cosAngle = cos(angle);
    float sinAngle = sin(angle);
    
    vec3 twistedPos;
    twistedPos.x = pos.x * cosAngle - pos.z * sinAngle;
    twistedPos.y = pos.y;
    twistedPos.z = pos.x * sinAngle + pos.z * cosAngle;
    
    fragPosition = modelMatrix * vec4(twistedPos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    // Rotar las normales también
    vec3 twistedNormal;
    twistedNormal.x = inNormals.x * cosAngle - inNormals.z * sinAngle;
    twistedNormal.y = inNormals.y;
    twistedNormal.z = inNormals.x * sinAngle + inNormals.z * cosAngle;
    
    fragNormal = normalize(vec3(modelMatrix * vec4(twistedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


# NUEVO SHADER 2: Wave Shader - Ondas sinusoidales múltiples
wave_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;
uniform float value;

void main()
{
    vec3 pos = inPosition;
    
    // Múltiples ondas con diferentes frecuencias y amplitudes
    float wave1 = sin(pos.x * 2.0 + time * 3.0) * value * 0.3;
    float wave2 = sin(pos.z * 3.0 - time * 2.0) * value * 0.2;
    float wave3 = cos((pos.x + pos.z) * 1.5 + time * 1.5) * value * 0.25;
    
    // Combinar ondas
    pos.y += wave1 + wave2 + wave3;
    
    // Ondas también en X y Z para mayor dinamismo
    pos.x += sin(pos.y * 2.0 + time) * value * 0.1;
    pos.z += cos(pos.y * 2.0 - time) * value * 0.1;
    
    fragPosition = modelMatrix * vec4(pos, 1.0);
    gl_Position = projectionMatrix * viewMatrix * fragPosition;
    
    // Calcular normales aproximadas basadas en las derivadas de las ondas
    vec3 tangentX = vec3(1.0, cos(pos.x * 2.0 + time * 3.0) * 2.0 * value * 0.3, 0.0);
    vec3 tangentZ = vec3(0.0, cos(pos.z * 3.0 - time * 2.0) * 3.0 * value * 0.2, 1.0);
    vec3 modifiedNormal = normalize(cross(tangentX, tangentZ));
    
    fragNormal = normalize(vec3(modelMatrix * vec4(modifiedNormal, 0.0)));
    fragTexCoords = inTexCoords;
}
'''


fat_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float value;


void main()
{
    fragPosition = modelMatrix * vec4(inPosition + inNormals * value, 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


water_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float displacement = sin(time + inPosition.x + inPosition.z) * value;
    fragPosition = modelMatrix * vec4(inPosition + vec3(0,displacement, 0)  , 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''



fat_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float value;


void main()
{
    fragPosition = modelMatrix * vec4(inPosition + inNormals * value, 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''


water_shader = '''
#version 330 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTexCoords;
layout (location = 2) in vec3 inNormals;

out vec2 fragTexCoords;
out vec3 fragNormal;
out vec4 fragPosition;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float value;


void main()
{
    float displacement = sin(time + inPosition.x + inPosition.z) * value;
    fragPosition = modelMatrix * vec4(inPosition + vec3(0,displacement, 0)  , 1.0);

    gl_Position = projectionMatrix * viewMatrix * fragPosition;

    fragNormal = normalize( vec3(modelMatrix * vec4(inNormals, 0.0)));

    fragTexCoords = inTexCoords;
}

'''