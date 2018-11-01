ballx = 300;
bally = 300;
ballvelx = 6*Math.random();
ballvely = 10;
ball2x = 300;
ball2y = 300;
ball2velx = 6*Math.random();
ball2vely = 1;
posX = 300;
var ctx;
var canvas;
document.onmousemove = handleMouse;
function init(){
	ballx = 300;
	bally = 300;
	ballvelx = 6*Math.random();
	ballvely = 10;
	posX = 300;
	ball2x = 500;
	ball2y = 500;
	ballvel2x = 6*Math.random();
	ballvel2y = 1;
	posX = 300;
	canvas = document.querySelector('.myCanvas');
	ctx = canvas.getContext('2d');
	ctx.fillStyle = 'rgb(0, 0, 0)';
	ctx.fillRect(0, 0, canvas.width, canvas.height);
	console.log(canvas.width);
	ctx.fillStyle = 'rgb(150,0,0)';
	fillCirc(200, 200, 25);
	ctx.fillStyle = 'green';
	ctx.fillRect(0,0,50,50);
	score = game();
}
function fillCirc(cx, cy, rad){
	ctx.beginPath();
	ctx.arc(cx, cy, rad, 0, 6.29, false);
	ctx.fill();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function game(){
	await sleep(500);
	score = 0;
	while(true){

		ballx += ballvelx;
		bally += ballvely;
		ballvely -= .1;

		if(ballx > canvas.width - 50 || ballx < 50){
			ballvelx *= -1;
		}

		if(bally > canvas.height - 50){
			ballvely *= -1;
			bally = canvas.height - 50;
		}

    	if(bally < 120 && Math.abs(posX-ballx) < 75){
    		ballvely *= -1;
    		bally = 120;
    		score += 100
    	}else if(bally < 120){
    		return endGame(score + 600 - Math.abs(posX-ballx));
    	}

    	ball2x += ball2velx;
		ball2y += ball2vely;
		ball2vely -= .1;

		if(ball2x > canvas.width - 20 || ball2x < 20){
			ball2velx *= -1;
		}

		if(ball2y > canvas.height - 50){
			ball2vely *= -1;
			ball2y = canvas.height - 50;
		}

		console.log("COND",Math.abs(posX-ball2x) < 75);
    	if(ball2y < 110 && Math.abs(posX-ball2x) < 75){
    		ball2vely *= -1;
    		ball2y = 110;
    	}else if(ball2y < 110){
    		return endGame(score + 600 - Math.abs(posX-ball2x));
    	}

		console.log(ballx,bally,ballvely);
		ctx.fillStyle = 'rgb(0, 0, 0)';
		ctx.fillRect(0, 0, canvas.width, canvas.height);
		ctx.fillStyle = 'rgb(150,0,0)';
		fillCirc(ballx, canvas.height-bally, 25);
    	console.log(ball2x,ball2y,ballvel2y);
		ctx.fillStyle = 'rgb(0,0,255)';
		fillCirc(ball2x, canvas.height-ball2y, 10);
    	ctx.fillStyle = 'rgb(150,150,150)';
    	ctx.fillRect(posX-50,500,100,5);

		ctx.fillStyle = 'green';
		ctx.fillRect(0,0,50,50);

		await sleep(10);
	}
}

function endGame(score){	
	ctx.fillStyle = 'rgb(50,50,50)';
	ctx.fillRect(0,0,50,50);
	ctx.fillStyle = 'rgb('+Math.round(score/30)+','+Math.round(score/30)+','+Math.round(score/30)+')';
	console.log(ctx.fillStyle);
	ctx.fillRect(canvas.width - 50,0,50,50);
}

function handleMouse(event){
	posX = event.clientX;
	// console.log(posX);
}