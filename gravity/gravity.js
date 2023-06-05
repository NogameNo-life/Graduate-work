var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var canvas_bg = document.getElementById('canvas_bg');
var context_bg = canvas_bg.getContext('2d');

var particles;
var numParticles = 300;
var walls;
var vfac = 1;
var t0, dt;
var g = 15;
var force;
var acc;

window.onload = init;

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function init() {
	particles = new Array();

	for(var i = 0; i < numParticles; i++){
		var radius = 7;

		var speed_x = getRandomArbitrary(0, 10);
		var speed_y = getRandomArbitrary(0, 10);

		if (Math.random() > 0.5) speed_x = (-1)*speed_x;
		if (Math.random() > 0.5) speed_y = (-1)*speed_y;

		var mass = 0.01*Math.pow(radius,3);
		var particle = new Particle(radius,'#5C62D6',mass,0);
		particle.pos2D = new Vector2D(Math.random()*(canvas.width-2*radius)+radius, Math.random()*(canvas.height-2*radius)+radius);

		particle.velo2D = new Vector2D(speed_x, speed_y);

		particles.push(particle);
		particle.draw(context);
	}

	walls = new Array();
	var wall1 = new Wall(new Vector2D(canvas.width,0),new Vector2D(0,0));
    wall1.draw(context_bg);
	walls.push(wall1);
	var wall2 = new Wall(new Vector2D(canvas.width,canvas.height),new Vector2D(canvas.width,0));
	wall2.draw(context_bg);
	walls.push(wall2);
	var wall3 = new Wall(new Vector2D(0,canvas.height),new Vector2D(canvas.width,canvas.height));
	wall3.draw(context_bg);
	walls.push(wall3);
	var wall4 = new Wall(new Vector2D(0,0),new Vector2D(0,canvas.height));
    wall4.draw(context_bg);
	walls.push(wall4);
	t0 = new Date().getTime();
	animFrame();
};

function animFrame(){
	animId = requestAnimationFrame(animFrame,canvas);
	onTimer();
}
function onTimer(){
	var t1 = new Date().getTime();
	dt = 0.0005*(t1-t0);
	t0 = t1;
	if (dt>0.2) {dt=0;};
	move();
}

function move(){
	context.clearRect(0, 0, canvas.width, canvas.height);
	for (var i=0; i<numParticles; i++){
		var particle = particles[i];
		calcForce(particle);
		updateAccel(particle);
		updateVelo(particle);
		moveObject(particle);
	}
	checkCollision();
}

function moveObject(obj){
	obj.pos2D = obj.pos2D.addScaled(obj.velo2D,dt);
	obj.draw(context);
}

function checkCollision(){
	for (var i=0; i<particles.length; i++){
		var particle1 = particles[i];
		for(var j=i+1; j<particles.length; j++){
			var particle2 = particles[j];
			var dist = particle1.pos2D.subtract(particle2.pos2D);
			if (dist.length() < (particle1.radius + particle2.radius) ) {
				// normal velocity vectors just before the impact
				var normalVelo1 = particle1.velo2D.project(dist);
				var normalVelo2 = particle2.velo2D.project(dist);
				// tangential velocity vectors
				var tangentVelo1 = particle1.velo2D.subtract(normalVelo1);
				var tangentVelo2 = particle2.velo2D.subtract(normalVelo2);
				// move particles so that they just touch
				var L = particle1.radius + particle2.radius-dist.length();
				var vrel = normalVelo1.subtract(normalVelo2).length();
				particle1.pos2D = particle1.pos2D.addScaled(normalVelo1,-L/vrel);
				particle2.pos2D = particle2.pos2D.addScaled(normalVelo2,-L/vrel);
				// normal velocity components after the impact
				var m1 = particle1.mass;
				var m2 = particle2.mass;
				var u1 = normalVelo1.projection(dist);
				var u2 = normalVelo2.projection(dist);
				var v1 = ((m1-m2)*u1+2*m2*u2)/(m1+m2);
				var v2 = ((m2-m1)*u2+2*m1*u1)/(m1+m2);
				// normal velocity vectors after collision
				normalVelo1 = dist.para(v1);
				normalVelo2 = dist.para(v2);
				// final velocity vectors after collision
				particle1.velo2D = normalVelo1.add(tangentVelo1);
				particle2.velo2D = normalVelo2.add(tangentVelo2);
			}
		}
		checkWallBounce(particle1);
	}
}
function checkWallBounce(obj){
	var hasHitAWall = false;
	for (var i=0; (i<walls.length && hasHitAWall==false); i++){
		var wall = walls[i];
		var wdir = wall.dir;
		var particlep1 = wall.p1.subtract(obj.pos2D);
		var particlep2 = wall.p2.subtract(obj.pos2D);
		var proj1 = particlep1.projection(wdir);
		var proj2 = particlep2.projection(wdir);
		var dist = particlep1.addScaled(wdir.unit(), proj1*(-1));
		var test = ((Math.abs(proj1) < wdir.length()) && (Math.abs(proj2) < wdir.length()));
		if ((dist.length() < obj.radius) &&  test){
			var angle = Vector2D.angleBetween(obj.velo2D, wdir);
			var normal = wall.normal;
			if (normal.dotProduct(obj.velo2D) > 0){
				normal.scaleBy(-1);
			}
			var deltaS = (obj.radius+dist.dotProduct(normal))/Math.sin(angle);
			var displ = obj.velo2D.para(deltaS);
			obj.pos2D = obj.pos2D.subtract(displ);
			var normalVelo = obj.velo2D.project(dist);
			var tangentVelo = obj.velo2D.subtract(normalVelo);
			obj.velo2D = tangentVelo.addScaled(normalVelo,-vfac);
			hasHitAWall = true;
		}
	}
}

function calcForce(obj){
	force = Forces.constantGravity(obj.mass,g);
}
function updateAccel(obj){
	acc = force.multiply(1/obj.mass);
}
function updateVelo(obj){
	obj.velo2D = obj.velo2D.addScaled(acc,dt);
}