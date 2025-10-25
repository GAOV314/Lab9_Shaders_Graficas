# GLSL

fragment_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


# NUEVO SHADER 1: Rainbow/Gradient Shader - Arcoíris dinámico animado
rainbow_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform float time;
uniform sampler2D tex0;

// Función para convertir HSV a RGB
vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main()
{
    // Crear un gradiente basado en posición y tiempo
    float hue = fract(fragPosition.x * 0.1 + fragPosition.y * 0.1 + fragPosition.z * 0.1 + time * 0.3);
    
    // Añadir ondas para hacer el arcoíris más dinámico
    hue += sin(fragPosition.y * 3.0 + time * 2.0) * 0.1;
    hue += cos(fragPosition.x * 2.0 - time * 1.5) * 0.1;
    
    // Variar saturación y brillo con el tiempo para efecto pulsante
    float saturation = 0.8 + sin(time * 3.0) * 0.2;
    float value = 0.9 + cos(time * 2.5) * 0.1;
    
    vec3 rainbowColor = hsv2rgb(vec3(hue, saturation, value));
    
    // Mezclar con la textura original
    vec3 texColor = texture(tex0, fragTexCoords).rgb;
    vec3 finalColor = mix(texColor, rainbowColor, 0.7);
    
    fragColor = vec4(finalColor, 1.0);
}
'''


# NUEVO SHADER 2: Procedural Pattern Shader - Patrones geométricos complejos
pattern_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform float time;
uniform sampler2D tex0;

// Función de ruido simplificado
float noise(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Patrón de Voronoi simplificado
float voronoi(vec2 p) {
    vec2 n = floor(p);
    vec2 f = fract(p);
    
    float minDist = 1.0;
    for(int j = -1; j <= 1; j++) {
        for(int i = -1; i <= 1; i++) {
            vec2 neighbor = vec2(float(i), float(j));
            vec2 point = noise(n + neighbor) * vec2(
                sin(time + noise(n + neighbor) * 6.28),
                cos(time + noise(n + neighbor) * 6.28)
            );
            vec2 diff = neighbor + point - f;
            float dist = length(diff);
            minDist = min(minDist, dist);
        }
    }
    return minDist;
}

// Patrón de cuadrícula hexagonal
float hexPattern(vec2 p) {
    p *= 8.0;
    vec2 s = vec2(1.0, 1.732);
    vec2 a = mod(p, s) - s * 0.5;
    vec2 b = mod(p - s * 0.5, s) - s * 0.5;
    return min(dot(a, a), dot(b, b));
}

void main()
{
    // Coordenadas para los patrones
    vec2 uv = fragPosition.xz * 2.0 + time * 0.1;
    
    // Combinar múltiples patrones
    float pattern1 = voronoi(uv * 3.0);
    float pattern2 = hexPattern(fragPosition.xy * 10.0 + time * 0.2);
    float pattern3 = sin(fragPosition.x * 10.0 + time) * cos(fragPosition.y * 10.0 - time);
    
    // Crear ondas circulares
    float dist = length(fragPosition.xz);
    float circles = sin(dist * 15.0 - time * 3.0) * 0.5 + 0.5;
    
    // Combinar patrones con pesos animados
    float combined = pattern1 * 0.3 + 
                     pattern2 * 0.3 + 
                     (pattern3 * 0.5 + 0.5) * 0.2 + 
                     circles * 0.2;
    
    // Colorear basado en los patrones
    vec3 color1 = vec3(0.2, 0.5, 1.0); // Azul
    vec3 color2 = vec3(1.0, 0.3, 0.5); // Rosa
    vec3 color3 = vec3(0.3, 1.0, 0.5); // Verde
    
    vec3 patternColor = mix(color1, color2, combined);
    patternColor = mix(patternColor, color3, sin(time + combined * 3.14) * 0.5 + 0.5);
    
    // Mezclar con textura base
    vec3 texColor = texture(tex0, fragTexCoords).rgb;
    vec3 finalColor = mix(texColor * 0.3, patternColor, 0.8);
    
    // Añadir brillo en las líneas del patrón
    float edge = smoothstep(0.45, 0.5, combined);
    finalColor += vec3(1.0) * edge * 0.5;
    
    fragColor = vec4(finalColor, 1.0);
}
'''


toon_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform vec3 pointLight;
uniform float ambientLight;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    if (intensity < 0.33)
        intensity = 0.2;
    else if (intensity < 0.66)
        intensity = 0.6;
    else
        intensity = 1.0;

    fragColor = texture(tex0, fragTexCoords) * intensity;
}

'''


negative_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;

void main()
{
    fragColor = 1 - texture(tex0, fragTexCoords);
}

'''


magma_shader = '''
#version 330 core

in vec2 fragTexCoords;
in vec3 fragNormal;
in vec4 fragPosition;

out vec4 fragColor;

uniform sampler2D tex0;
uniform sampler2D tex1;

uniform vec3 pointLight;
uniform float ambientLight;

uniform float time;

void main()
{
    vec3 lightDir = normalize(pointLight - fragPosition.xyz);
    float intensity = max( 0 , dot(fragNormal, lightDir)) + ambientLight;

    fragColor = texture(tex0, fragTexCoords) * intensity;
    fragColor += texture(tex1, fragTexCoords) * ((sin(time) + 1) / 2);
}

'''



