/*
 *  cmainext.cp
 *  C++ extension for TimeSplitters Platinum. Intergration by ctypes
 *
 *  Created by Matthew Mitchell on 23/05/2010.
 *  Copyright 2010 Matthew Mitchell. All rights reserved.
 *
 */
#include <vector>
#include <OpenGL/gl.h>
#include <iostream>
using namespace std;
struct SnowData {
	GLdouble x;
	GLdouble y;
	GLdouble z;
	int tex;
};
float windx = 0;
float windz = 0;
vector<SnowData> snow_data;
GLuint snow_texture;
extern "C" void add_snow_texture(GLuint texture){
	snow_texture = texture;
}
extern "C" void draw_snow(int fps){
	float decent = 3.5/fps; //holds the rate of descent
	//Change wind
	windx +=  (0.2*((float)rand()/RAND_MAX))-0.1;
	windz +=  (0.2*((float)rand()/RAND_MAX))-0.1;
	if (windx > 2){
		windx = 2;
	}else if (windx < 0) {
		windx = -2;
	}
	if (windz > 2){
		windz = 2;
	}else if (windz < 0) {
		windz = -2;
	}
	//Run through, remove fallen snowflakes and change position of others
	for (int x = 0; x < snow_data.size(); x++){
		if (snow_data[x].y > -3){
			//Change position of snowflake
			snow_data[x].y -= decent;
			snow_data[x].x += (windx + (1*((float)rand()/RAND_MAX))-0.5)/fps;
			snow_data[x].z += (windz + (1*((float)rand()/RAND_MAX))-0.5)/fps;
		}else{
			snow_data.erase(snow_data.begin() + x);
			x -= 1;
		}
	}
	SnowData flake_data; 
	for (int x = 0; x < 2000.0/fps; x++){
		//Emit 2000 snowflakes per second
		flake_data.x = (40*((float)rand()/RAND_MAX))-10;
		flake_data.y = 21;
		flake_data.z = (rand() % 180 - 10);
		flake_data.tex = (rand() % 3);
		snow_data.push_back(flake_data); 
	}
	//Render all the snowflakes
	glDisable(GL_CULL_FACE);
	GLfloat colour[] = {1, 1, 1, 1}; 
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
	glBindTexture(GL_TEXTURE_2D, snow_texture);
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colour);
	glEnableClientState(GL_VERTEX_ARRAY);
	glEnableClientState(GL_TEXTURE_COORD_ARRAY);
	//Make array with coordinates to work with glVertexPointer
	GLdouble snow_flake_vertices_array[snow_data.size()][12];
	GLdouble snow_flake_texcoord_array[snow_data.size()][8];
	for (int x = 0; x < snow_data.size(); x++) {
		snow_flake_vertices_array[x][0] = snow_data[x].x - 0.05;
		snow_flake_vertices_array[x][1] = snow_data[x].y - 0.05;
		snow_flake_vertices_array[x][2] = snow_data[x].z;
		snow_flake_texcoord_array[x][0] = 0.25 * snow_data[x].tex;
		snow_flake_texcoord_array[x][1] = 0.0;
		snow_flake_vertices_array[x][3] = snow_data[x].x + 0.05;
		snow_flake_vertices_array[x][4] = snow_data[x].y - 0.05;
		snow_flake_vertices_array[x][5] = snow_data[x].z;
		snow_flake_texcoord_array[x][2] = 0.25 * snow_data[x].tex + 0.25;
		snow_flake_texcoord_array[x][3] = 0.0;
		snow_flake_vertices_array[x][6] = snow_data[x].x + 0.05;
		snow_flake_vertices_array[x][7] = snow_data[x].y + 0.05;
		snow_flake_vertices_array[x][8] = snow_data[x].z;
		snow_flake_texcoord_array[x][4] = 0.25 * snow_data[x].tex + 0.25;
		snow_flake_texcoord_array[x][5] = 1.0;
		snow_flake_vertices_array[x][9] = snow_data[x].x - 0.05;
		snow_flake_vertices_array[x][10] = snow_data[x].y + 0.05;
		snow_flake_vertices_array[x][11] = snow_data[x].z;
		snow_flake_texcoord_array[x][6] = 0.25 * snow_data[x].tex;
		snow_flake_texcoord_array[x][7] = 1.0;
	}
	glVertexPointer(3, GL_DOUBLE, 0, &snow_flake_vertices_array);
	glTexCoordPointer(2, GL_DOUBLE, 0, &snow_flake_texcoord_array);
	glDrawArrays(GL_QUADS, 0, snow_data.size() * 4);
	glDisableClientState(GL_TEXTURE_COORD_ARRAY);
	glDisableClientState(GL_VERTEX_ARRAY);
	glEnable(GL_CULL_FACE);
}

