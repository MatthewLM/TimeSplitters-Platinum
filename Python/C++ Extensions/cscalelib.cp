/*
 *  cscalelib.cp
 *  C++ extension for cscalelib. Intergration by ctypes
 *
 *  Created by Matthew Mitchell on 23/05/2010.
 *  Copyright 2010 Matthew Mitchell.
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 */
#define BOX_TEXCOORDS 2
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <iostream>
#include <math.h> //Should be maths.h 
#include <stdio.h>
using namespace std;
GLdouble arc_factors[][2] = {{1.0, 0.0}, {0.99984769515639127, 0.017452406437283512}, {0.99939082701909576, 0.034899496702500969}, {0.99862953475457383, 0.052335956242943835}, {0.9975640502598242, 0.069756473744125302}, {0.99619469809174555, 0.087155742747658166}, {0.99452189536827329, 0.10452846326765347}, {0.99254615164132198, 0.12186934340514748}, {0.99026806874157036, 0.13917310096006544}, {0.98768834059513777, 0.15643446504023087}, {0.98480775301220802, 0.17364817766693033}, {0.98162718344766398, 0.1908089953765448}, {0.97814760073380569, 0.20791169081775934}, {0.97437006478523525, 0.224951054343865}, {0.97029572627599647, 0.24192189559966773}, {0.96592582628906831, 0.25881904510252074}, {0.96126169593831889, 0.27563735581699916}, {0.95630475596303544, 0.29237170472273677}, {0.95105651629515353, 0.3090169943749474}, {0.94551857559931685, 0.3255681544571567}, {0.93969262078590843, 0.34202014332566871}, {0.93358042649720174, 0.35836794954530027}, {0.92718385456678742, 0.37460659341591201}, {0.92050485345244037, 0.39073112848927377}, {0.91354545764260087, 0.40673664307580021}, {0.90630778703664994, 0.42261826174069944}, {0.89879404629916704, 0.4383711467890774}, {0.8910065241883679, 0.45399049973954675}, {0.88294759285892699, 0.46947156278589081}, {0.87461970713939574, 0.48480962024633706}, {0.86602540378443871, 0.49999999999999994}, {0.85716730070211233, 0.51503807491005416}, {0.84804809615642596, 0.5299192642332049}, {0.83867056794542405, 0.54463903501502708}, {0.82903757255504162, 0.5591929034707469}, {0.8191520442889918, 0.57357643635104605}, {0.80901699437494745, 0.58778525229247314}, {0.79863551004729283, 0.60181502315204827}, {0.7880107536067219, 0.61566147532565829}, {0.7771459614569709, 0.62932039104983739}, {0.76604444311897812, 0.64278760968653925}, {0.75470958022277201, 0.65605902899050728}, {0.74314482547739424, 0.66913060635885824}, {0.73135370161917046, 0.68199836006249848}, {0.71933980033865119, 0.69465837045899725}, {0.70710678118654757, 0.70710678118654746}, {0.70710678118654746, 0.70710678118654757}, {0.69465837045899725, 0.71933980033865119}, {0.68199836006249848, 0.73135370161917046}, {0.66913060635885824, 0.74314482547739424}, {0.65605902899050728, 0.75470958022277201}, {0.64278760968653925, 0.76604444311897812}, {0.62932039104983739, 0.7771459614569709}, {0.61566147532565829, 0.7880107536067219}, {0.60181502315204827, 0.79863551004729283}, {0.58778525229247314, 0.80901699437494745}, {0.57357643635104605, 0.8191520442889918}, {0.5591929034707469, 0.82903757255504162}, {0.54463903501502708, 0.83867056794542405}, {0.5299192642332049, 0.84804809615642596}, {0.51503807491005416, 0.85716730070211233}, {0.49999999999999994, 0.86602540378443871}, {0.48480962024633706, 0.87461970713939574}, {0.46947156278589081, 0.88294759285892699}, {0.45399049973954675, 0.8910065241883679}, {0.4383711467890774, 0.89879404629916704}, {0.42261826174069944, 0.90630778703664994}, {0.40673664307580021, 0.91354545764260087}, {0.39073112848927377, 0.92050485345244037}, {0.37460659341591201, 0.92718385456678742}, {0.35836794954530027, 0.93358042649720174}, {0.34202014332566871, 0.93969262078590843}, {0.3255681544571567, 0.94551857559931685}, {0.3090169943749474, 0.95105651629515353}, {0.29237170472273677, 0.95630475596303544}, {0.27563735581699916, 0.96126169593831889}, {0.25881904510252074, 0.96592582628906831}, {0.24192189559966773, 0.97029572627599647}, {0.224951054343865, 0.97437006478523525}, {0.20791169081775934, 0.97814760073380569}, {0.1908089953765448, 0.98162718344766398}, {0.17364817766693033, 0.98480775301220802}, {0.15643446504023087, 0.98768834059513777}, {0.13917310096006544, 0.99026806874157036}, {0.12186934340514748, 0.99254615164132198}, {0.10452846326765347, 0.99452189536827329}, {0.087155742747658166, 0.99619469809174555}, {0.069756473744125302, 0.9975640502598242}, {0.052335956242943835, 0.99862953475457383}, {0.034899496702500969, 0.99939082701909576}, {0.017452406437283512, 0.99984769515639127}, {0.0, 1.0}};
extern "C" void setup_framebuffer(bool flip,GLuint frame_buffer_id,GLuint texture_id,int width,int height){
	glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, frame_buffer_id);
	glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, GL_TEXTURE_2D, texture_id, 0);
	glPushAttrib(GL_VIEWPORT_BIT);
	glViewport(0,0,width,height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity(); //Load the projection matrix
	if (flip){
		gluOrtho2D(0,width,height,0);
	}else{
		gluOrtho2D(0,width,0,height);
	}
}
extern "C" void end_framebuffer(){
	glPopAttrib();
	glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, 0);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity(); //Load the projection matrix
	gluOrtho2D(0,1280,720,0); //Set an orthorgraphic view
}
extern "C" void add_lines(bool antialias,GLdouble coordinates[][2],int array_size,GLdouble w,GLdouble r,GLdouble g, GLdouble b,GLdouble a){
	glDisable(GL_TEXTURE_2D);
	if (antialias){
		glEnable(GL_LINE_SMOOTH); //Enable line smoothing.
	}
	glColor4d(r/255,g/255,b/255,a/255);
	glLineWidth(w);
	GLuint vbo;
	glGenBuffers(1, &vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	GLsizeiptr vertex_size = array_size*2*sizeof(GLdouble);
	GLdouble vertices[array_size * 2];
	int index = 0;
	for (int x = 0; x < array_size; x++) {
		vertices[index] = coordinates[x][0];
		vertices[index + 1] = coordinates[x][1];
		index = index + 2;
	}
	glBufferData(GL_ARRAY_BUFFER, vertex_size, vertices, GL_STATIC_DRAW);
	glVertexPointer(2, GL_DOUBLE, 0, 0);
	glEnableClientState(GL_VERTEX_ARRAY);
	glDrawArrays(GL_LINE_STRIP, 0, array_size);
	glDisableClientState(GL_VERTEX_ARRAY);
	glDeleteBuffers(1,&vbo);
	if (antialias){
		glDisable(GL_LINE_SMOOTH); //Disable line smoothing.
	}
	glEnable(GL_TEXTURE_2D);
}
extern "C" GLuint * create_box_vbo(GLdouble size[2]){
	GLuint vbo;
	glGenBuffers(1,&vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	GLsizeiptr data_size = 8*sizeof(GLdouble);
	GLdouble vertices[] = {0,0,  0,size[1],  size[0],0,  size[0],size[1]};
	glBufferData(GL_ARRAY_BUFFER, data_size, vertices, GL_STATIC_DRAW);
	GLuint * result = new GLuint[2]; //New array for VBO
	result[0] =vbo; //Assign data
	result[1] = 4; 
	return result; //Return data
}
struct VertexData2D{
	GLdouble x,y,s,t;
};
struct VertexData3D{
	GLdouble x,y,z,s,t;
};
extern "C" GLuint * create_rounded_corners_vbo(GLdouble size[2],GLdouble rounded,GLint sides){
	short int bits_set = (sides & 1) + (sides & 2)/2 + (sides & 4)/4 + (sides & 8)/8;
	GLuint vertex_num = 91*bits_set + 4; //Number of vertices needed
	VertexData2D data[vertex_num];
	int array_pos = 0;
	if (sides & 1){
		for (int x = 0;x<91;x++){
			data[array_pos].x = (1 - arc_factors[x][0]) * rounded;
			data[array_pos].y = (1 - arc_factors[x][1]) * rounded;
			data[array_pos].s = data[array_pos].x/size[0];
			data[array_pos].t = data[array_pos].y/size[1];
			array_pos++;
		}
	}else{
		data[array_pos].x = 0;
		data[array_pos].y = 0;
		data[array_pos].s = 0;
		data[array_pos].t = 0;
		array_pos++;
	}
	if (sides & 2){
		for (int x = 91;x>=0;x--){
			data[array_pos].x = size[0] - (1 - arc_factors[x][0]) * rounded;
			data[array_pos].y = (1 - arc_factors[x][1]) * rounded;
			data[array_pos].s = data[array_pos].x/size[0];
			data[array_pos].t = data[array_pos].y/size[1];
			array_pos++;
		}
	}else{
		data[array_pos].x = size[0];
		data[array_pos].y = 0;
		data[array_pos].s = 1;
		data[array_pos].t = 0;
		array_pos++;
	}
	if (sides & 4){
		for (int x = 0;x<91;x++){
			data[array_pos].x = size[0] - (1 - arc_factors[x][0]) * rounded;
			data[array_pos].y = size[1] - (1 - arc_factors[x][1]) * rounded;
			data[array_pos].s = data[array_pos].x/size[0];
			data[array_pos].t = data[array_pos].y/size[1];
			array_pos++;
		}
	}else{
		data[array_pos].x = size[0];
		data[array_pos].y = size[1];
		data[array_pos].s = 1;
		data[array_pos].t = 1;
		array_pos++;
	}
	if (sides & 8){
		for (int x = 91;x>=0;x--){
			data[array_pos].x= (1 - arc_factors[x][0]) * rounded;
			data[array_pos].y = size[1] - (1 - arc_factors[x][1]) * rounded;
			data[array_pos].s = data[array_pos].x/size[0];
			data[array_pos].t = data[array_pos].y/size[1];
			array_pos++;
		}
	}else{
		data[array_pos].x = 0;
		data[array_pos].y = size[1];
		data[array_pos].s = 0;
		data[array_pos].t = 1;
		array_pos++;
	}
	GLuint vbo;
	glGenBuffers(1,&vbo);
	glBindBuffer(GL_ARRAY_BUFFER, vbo);
	glBufferData(GL_ARRAY_BUFFER, sizeof(data), (GLvoid*)data, GL_STATIC_DRAW);
	GLuint * result = new GLuint[2]; //New array for VBO data
	result[0] =vbo; //Assign data
	result[1] = vertex_num; 
	return result; //Return data
}
extern "C" void delete_vbo(GLuint vbo[2]){
	glDeleteBuffers(1,&vbo[0]);
	delete [] vbo; //Free the memory used by thr VBO data.
}
extern "C" void draw_texture(GLuint texture,GLdouble offset[2],GLdouble size[2],GLdouble a,short int sides,GLdouble angle,GLdouble point[2],GLint vbo[2],GLdouble scalex,GLdouble scaley){
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);
	glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
	glColor4d(1,1,1,a/255);
	glBindTexture(GL_TEXTURE_2D, texture);
	glMatrixMode(GL_TEXTURE);
	glLoadIdentity();
	if (angle != 0){
		glRotatef(angle,point[0],point[1],0);
	}
	glScaled(scalex,scaley,0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glTranslated(offset[0],offset[1],0);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	if(sides == 0){
		glVertexPointer(2, GL_DOUBLE, 0, 0);
		glBindBuffer(GL_ARRAY_BUFFER,BOX_TEXCOORDS);
		glTexCoordPointer (2, GL_INT, 0, 0);
	}else{
		glVertexPointer(2, GL_DOUBLE, sizeof(GLdouble)*4, (GLvoid*)offsetof(VertexData2D, x));
		glTexCoordPointer(2, GL_DOUBLE, sizeof(GLdouble)*4, (GLvoid*)offsetof(VertexData2D, s));
	}
	glEnableClientState(GL_VERTEX_ARRAY);
	glEnableClientState(GL_TEXTURE_COORD_ARRAY);
	if(sides == 0){
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glDrawArrays(GL_TRIANGLES, 1, 3);
	}else{
		glDrawArrays(GL_POLYGON, 0, vbo[1]);
	}
	glDisableClientState(GL_TEXTURE_COORD_ARRAY);
	glDisableClientState(GL_VERTEX_ARRAY);
	glBindBuffer(GL_ARRAY_BUFFER, 0);
}
GLdouble * normalise(GLdouble v[4][3]){
	GLdouble a[3];
	GLdouble b[3];
	GLdouble * normal = new GLdouble[3];
	a[0] = v[0][0] - v[1][0];
	a[1] = v[0][1] - v[1][1];
	a[2] = v[0][2] - v[1][2];
	b[0] = v[1][0] - v[2][0];
	b[1] = v[1][1] - v[2][1];
	b[2] = v[1][2] - v[2][2];
	normal[0] = (a[1] * b[2]) - (a[2] * b[1]);
	normal[1] = (a[2] * b[0]) - (a[0] * b[2]);
	normal[2] = (a[0] * b[1]) - (a[1] * b[0]);
	GLdouble len = (sqrt((normal[0] * normal[0]) + (normal[1] * normal[1]) + (normal[2] * normal[2])));
	if (len == 0.0f){
		len = 1.0f;
	}
	normal[0] /= -len;
	normal[1] /= -len;
	normal[2] /= -len;
	return normal;
}
extern "C" void draw_rectangle(GLdouble vertices[4][3],GLfloat colour[4]){
	glDisable(GL_CULL_FACE);
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colour);
	glEnableClientState(GL_VERTEX_ARRAY);
	glVertexPointer(3, GL_DOUBLE, 0, vertices);
	glDrawArrays(GL_TRIANGLES, 0, 3);
	glDrawArrays(GL_TRIANGLES, 1, 3);
	glDisableClientState(GL_VERTEX_ARRAY);
	glEnable(GL_CULL_FACE);
}
extern "C" GLuint make_rectangle(GLdouble vertices[4][3],GLdouble tex_w,GLdouble tex_h,GLfloat colour[4]){ //tex_w and tex_h is the number of texture repeats over the width and height
	GLuint display_list = glGenLists(1);
	glNewList(display_list, GL_COMPILE);
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, colour);
	glBegin(GL_QUADS);
	GLdouble * norm = normalise(vertices);
	glTexCoord2d(0,0); glVertex3dv(vertices[0]); glNormal3dv(norm);
	glTexCoord2d(tex_w,0); glVertex3dv(vertices[1]); glNormal3dv(norm);
	glTexCoord2d(tex_w,tex_h); glVertex3dv(vertices[2]); glNormal3dv(norm);
	glTexCoord2d(0,tex_h); glVertex3dv(vertices[3]); glNormal3dv(norm);
	glEnd();
	glEndList();
	return display_list;
}

/* extern "C" GLuint make_circle(GLdouble centre[3],GLdouble radius,GLdouble texture_radius,GLdouble colour[4]){
	GLuint display_list = glGenLists(1);
	glNewList(display_list, GL_COMPILE);
	glColor4dv(colour);
	glBegin(GL_POLYGON);
	for (int x = 0;x<91;x++){
		data[array_pos].x = (1 - arc_factors[x][0]) * rounded;
		data[array_pos].y = (1 - arc_factors[x][1]) * rounded;
		data[array_pos].s = data[array_pos].x/size[0];
		data[array_pos].t = data[array_pos].y/size[1];
		array_pos++;
	for (int x = 91;x>=0;x--){
		data[array_pos].x = size[0] - (1 - arc_factors[x][0]) * rounded;
		data[array_pos].y = (1 - arc_factors[x][1]) * rounded;
		data[array_pos].s = data[array_pos].x/size[0];
		data[array_pos].t = data[array_pos].y/size[1];
		array_pos++;
	for (int x = 0;x<91;x++){
		data[array_pos].x = size[0] - (1 - arc_factors[x][0]) * rounded;
		data[array_pos].y = size[1] - (1 - arc_factors[x][1]) * rounded;
		data[array_pos].s = data[array_pos].x/size[0];
		data[array_pos].t = data[array_pos].y/size[1];
		array_pos++;
	}
	for (int x = 91;x>=0;x--){
		data[array_pos].x= (1 - arc_factors[x][0]) * rounded;
		data[array_pos].y = size[1] - (1 - arc_factors[x][1]) * rounded;
		data[array_pos].s = data[array_pos].x/size[0];
		data[array_pos].t = data[array_pos].y/size[1];
		array_pos++;
	}
	glTexCoord2d(0,0); glVertex3dv(vertices[0]);
	glTexCoord2d(tex_w,0); glVertex3dv(vertices[1]);
	glTexCoord2d(tex_w,tex_h); glVertex3dv(vertices[2]);
	glTexCoord2d(0,tex_h); glVertex3dv(vertices[3]);
	glEnd();
	glEndList();
	return display_list;
} */
extern "C" void draw_list(GLuint display_list,GLuint texture){
	glBindTexture(GL_TEXTURE_2D, texture);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glCallList(display_list);
	glBindTexture(GL_TEXTURE_2D, 0);
}
/* extern "C" GLuint * load_image_texture( texture){
 GLuint * texture_data = new GLuint[3];
 //Get image data
 
 //Make texture with data
 glGenTextures(1, &texture_data[0]);
 glMatrixMode(GL_MODELVIEW);
 glLoadIdentity();
 glBindTexture(GL_TEXTURE_2D, texture_data[0]);
 glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
 glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
 glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
 gluBuild2DMipmaps( GL_TEXTURE_2D, 3, texture_data[1], texture_data[2],GL_RGBA, GL_UNSIGNED_BYTE,image_data);
 return texture_data;
 } */