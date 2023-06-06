function Forces(){
}

// STATIC METHODS
Forces.constantGravity = function(m,g){
	return new Vector2D(0,m*g);
}
Forces.gravity = function(G,m1,m2,r){
	return r.multiply(-G*m1*m2/(r.lengthSquared()*r.length()));
}
Forces.gravityModified = function(G,m1,m2,r,eps){
	return r.multiply(-G*m1*m2/((r.lengthSquared()+eps*eps)*r.length()));
}

