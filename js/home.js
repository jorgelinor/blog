var canvas = document.getElementById('marioGG'),  
    ctx = canvas.getContext("2d")
    i = 0; 

function drawMarioGG (cCap0,cCap1,cCap3,cCap4) {
  
  if (!cCap0 || !cCap1 || !cCap3 || !cCap4){
  	var colorCap0 = '#fd1316';
		var colorCap1 = '#890105';
		var colorCap3 = '#6e0001';
		var colorCap4 = '#890105';
	}
	else  {
		var colorCap0 = cCap0;
		var colorCap1 = cCap1;
		var colorCap3 = cCap4;
		var colorCap4 = cCap3;
	}
	

	ctx.clearRect(0, 0, canvas.width, canvas.height);


	
	//The face ------------------------------------------------------------------
		
		grad = ctx.createRadialGradient(100,100,0,100,100,500); 
		grad.addColorStop(0, "#ffecb7");
		grad.addColorStop(1, "#ba8365");


		
		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(62, 216); 
		
		ctx.quadraticCurveTo(200,100,350, 216);
		ctx.lineTo(336, 303);
		ctx.bezierCurveTo(330,300, 380, 400,264, 433);
		ctx.quadraticCurveTo(200,480,140, 433);
		ctx.bezierCurveTo(20,410, 67, 300,62, 303);
		ctx.lineTo(62, 216);
	
		

		ctx.fill(); 
		
	// Ears ---------------------------------------------------------------------------------------------------------		
		
	// Left ear
	
		grad = ctx.createLinearGradient(25,22,51,362)
		grad.addColorStop(0, "#c67862");
		grad.addColorStop(1, "#fee7b3");
			
		
		
		ctx.fillStyle = grad;
		
		ctx.beginPath()
		ctx.moveTo(60, 364); 
		
		ctx.bezierCurveTo(54,365, 10, 360,4, 290);
		ctx.bezierCurveTo(0,230, 40,246,55, 259);
	
		ctx.fill();
		
		
		rad = ctx.createLinearGradient(25,274,51,332)
		grad.addColorStop(0, "#9d563f");
		grad.addColorStop(1, "#fee7b3");
	
		
		ctx.fillStyle = grad;
		
		
		ctx.beginPath()
		ctx.moveTo(49, 326); 
		
		ctx.bezierCurveTo(10,345, 10, 260,21, 268);
		ctx.bezierCurveTo(20,250, 40,266,48, 300);
	
		ctx.fill();
		
	// End Left Ear
		
	//Right ear
	
		grad = ctx.createLinearGradient(25,22,51,362)
		grad.addColorStop(0, "#ba8365");
		grad.addColorStop(1, "#cb9279");
			
		
		
		ctx.fillStyle = grad;
		
		ctx.beginPath()
		ctx.moveTo(338, 364); 
		
		ctx.bezierCurveTo(390,355, 390, 330,396, 290);
		ctx.bezierCurveTo(400,230, 350,246,345, 260);
	
		ctx.fill();
		
		
		rad = ctx.createLinearGradient(325,224,351,302)
		grad.addColorStop(0, "#553426");
		grad.addColorStop(1, "#ba8365");
	

		ctx.fillStyle = grad;
		
		
		ctx.beginPath()
		ctx.moveTo(349, 330); 
		
		ctx.bezierCurveTo(400,345, 390, 260,381, 263);
		ctx.bezierCurveTo(370,250, 360,266,352, 300);
	
		ctx.fill();
		
	//end Right ear
		
	// Left sideburn 
	
		grad = ctx.createLinearGradient(47,281,73,289)
		grad.addColorStop(0, "#5c1500");
		grad.addColorStop(1, "#812705");


		
		
		
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(70, 210); 
		
		ctx.bezierCurveTo(60,240, 90, 305,64, 308);
		ctx.quadraticCurveTo(62,319,59, 329);
		ctx.bezierCurveTo(40,325, 50, 305,45, 249);
		ctx.quadraticCurveTo(62,210,70, 210);
		
		
		ctx.fill(); 
		
		// right sideburn 
	
		grad = ctx.createLinearGradient(330,263,354,276)
		grad.addColorStop(0, "#220a00");
		grad.addColorStop(1, "#481801");


		
		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(330, 203); 
		

		ctx.quadraticCurveTo(340,190,357, 230);
		ctx.bezierCurveTo(354,345, 355, 315,342, 330);
		ctx.bezierCurveTo(335,330, 340, 330,335, 305);
		ctx.bezierCurveTo(320,270, 335, 300,330, 203);
	
		
		
		ctx.fill(); 
	
	// left eyebrow 
	
		grad = ctx.createLinearGradient(132,184,131,202)
		grad.addColorStop(0, "#220a00");
		grad.addColorStop(1, "#481801");


		
		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(99, 222); 
		
		ctx.bezierCurveTo(110,145, 155,155,171, 227);
		ctx.bezierCurveTo(135,205, 148,193,99, 222);
		
		
		ctx.fill(); 
		
		// right eyebrow 
	
		grad = ctx.createLinearGradient(132,184,131,202)
		grad.addColorStop(0, "#220a00");
		grad.addColorStop(1, "#481801");

		
		
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(230, 228); 
		
		ctx.bezierCurveTo(250,145, 295,155,302, 222);
		ctx.bezierCurveTo(270,205, 263,193,230, 228);
		
		
		
		ctx.fill(); 
		
		// Left eye -------------------------------------------------------------------------------------------------------
	
	
		// white
		
		grad = ctx.createLinearGradient(140,313,144,227)
		grad.addColorStop(0, "#dad4d6");
		grad.addColorStop(1, "#ffffff");
		

		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(140, 313); 
		
		ctx.bezierCurveTo(94,307, 110,229,144, 227);
		ctx.bezierCurveTo(177,220,197,300,140, 313);
		
		ctx.fill();
		
		
		// light blue
		grad = ctx.createRadialGradient(157,285,0,159,285,59); 
		grad.addColorStop(0, "#297bd1");
		grad.addColorStop(1, "#00edfe");
		
		

		

		ctx.fillStyle = grad;
		ctx.strokeStyle = "#3580b7";
		ctx.lineWidth = 2;
		ctx.beginPath()
		ctx.moveTo(144, 305); 
		
		ctx.bezierCurveTo(137,310, 110,246,156, 239);
		ctx.bezierCurveTo(185,235,183,310,144, 305);
		ctx.stroke();
		ctx.fill();
		
		// black

		
	
		ctx.fillStyle = "#000000";
	

		ctx.beginPath()
		ctx.moveTo(150, 300); 
		
		ctx.bezierCurveTo(155,310, 120,256,155, 249);
		ctx.bezierCurveTo(167,250, 190,276,150, 300);

	
		ctx.fill();
		
		// white spot
		grad = ctx.createRadialGradient(158,263,0,156,263,5); 
		grad.addColorStop(0, "#ffffff");
		grad.addColorStop(0.96,"#336ba4");
		grad.addColorStop(1, "#000000");
		
	
		ctx.fillStyle = grad;
	

		ctx.beginPath()
		ctx.moveTo(150, 300); 
		
		ctx.arc(157,263,5,0,Math.PI*2,true);

	
		ctx.fill();
		
		// Blue spot
		
		grad = ctx.createRadialGradient(158,282,0,156,282,7); 
		grad.addColorStop(0, "#170cd4");
		grad.addColorStop(1, "#000000");
		
		
		ctx.fillStyle = grad;
	

		ctx.beginPath()
		ctx.moveTo(150, 283); 
		
		ctx.arc(157, 283,7,0,Math.PI*2,true);

	
		ctx.fill();
		
	// Right eye -------------------------------------------------------------------------------------------------------
	
	
		// white
		
		grad = ctx.createLinearGradient(140,313,144,227)
		grad.addColorStop(0, "#dad4d6");
		grad.addColorStop(1, "#ffffff");
		

		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(227, 283); 
		
		ctx.bezierCurveTo(224,217, 265,209,284, 247);
		ctx.bezierCurveTo(287,250,297,310,261, 313);
		
		ctx.fill();
		
		
		// light blue
		grad = ctx.createRadialGradient(227,285,0,259,285,59); 
		grad.addColorStop(0, "#297bd1");
		grad.addColorStop(1, "#00edfe");
		
		

		ctx.fillStyle = grad;
		ctx.strokeStyle = "#3580b7";
		ctx.lineWidth = 2;
		ctx.beginPath()
		ctx.moveTo(227, 283); 
		
		ctx.bezierCurveTo(227,260, 230,226,260, 246);
		ctx.bezierCurveTo(267,252,283,290,258, 308);
		ctx.stroke();
		ctx.fill();
		
		// black

		
	
		ctx.fillStyle = "#000000";
	

		ctx.beginPath()
		ctx.moveTo(231, 285); 
		
		ctx.bezierCurveTo(235,290, 220,246,251, 250);
		ctx.bezierCurveTo(257,250, 270,276,252, 297);

		ctx.fill(); 
		
		// white spot
		grad = ctx.createRadialGradient(247,263,0,246,263,7); 
		grad.addColorStop(0, "#ffffff");
		grad.addColorStop(0.99,"#336ba4");
		grad.addColorStop(1, "#000000");
		
		
		ctx.fillStyle = grad;
	

		ctx.beginPath()
	
		
		ctx.arc(245,263,7,0,Math.PI*2,true);

	
		ctx.fill();
		
		// Blue spot
		
		grad = ctx.createRadialGradient(245,282,0,245,282,7); 
		grad.addColorStop(0, "#170cd4");
		grad.addColorStop(1, "#000000");
		
		
		ctx.fillStyle = grad;
	

		ctx.beginPath()
	
		ctx.arc(246, 283,7,0,Math.PI*2,true);

	
		ctx.fill();
		
		//End eyes  -------------------------------------------------------------------------------------------------------
		
		//mustache -------------------------------------------------------------------------------------------------------
		
		grad = ctx.createRadialGradient(157,323,0,157,323,200); 
		grad.addColorStop(0, "#28160c");
		grad.addColorStop(1, "#702404");
		
		

		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(91, 300); 
		
		ctx.bezierCurveTo(100,345, 300, 345,310, 300);
		ctx.bezierCurveTo(320,320, 330, 350,294, 360);
		ctx.bezierCurveTo(300,390, 250, 390,251, 380);
		ctx.bezierCurveTo(230,410, 200, 390,200, 390);
		ctx.bezierCurveTo(180,410, 150, 390,151, 380);
		ctx.bezierCurveTo(140,390, 100, 380,108, 360);
		ctx.bezierCurveTo(100,365, 70, 335,91, 300);
	
	

		ctx.fill(); 
		
		// end mustache -------------------------------------------------------------------------------------------------------
		
		//Lips -------------------------------------------------------------------------------------------------------
		
		grad = ctx.createRadialGradient(200,400,0,200,400,50); 
		grad.addColorStop(0, "#600002");
		grad.addColorStop(1, "#000000");
	
		
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(145, 380); 
		
		ctx.bezierCurveTo(130,415, 270, 415,255, 380);
		ctx.bezierCurveTo(270, 410,130,410, 145, 380);
	

		ctx.fill(); 
		
		// end lips -------------------------------------------------------------------------------------------------------
		
		//chin -------------------------------------------------------------------------------------------------------
		
		grad = ctx.createRadialGradient(170,425,0,170,425,80); 
		grad.addColorStop(0, "#d0a580");
		grad.addColorStop(1, "#c09674");
	
		

		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(175, 420); 
		
		ctx.bezierCurveTo(150,425, 260, 435,225, 420);
		ctx.bezierCurveTo(220, 420,120,429, 175, 420);
	

		ctx.fill(); 
		
		// end chin -------------------------------------------------------------------------------------------------------
		
		
		//nose -------------------------------------------------------------------------------------------------------
		
		grad = ctx.createRadialGradient(157,333,0,157,333,80); 
		grad.addColorStop(0, "#fef9c2");
		grad.addColorStop(1, "#ba8365");


		
		

		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(137, 333); 
		
		ctx.bezierCurveTo(140,260, 260, 260,264, 333);
		ctx.bezierCurveTo(260,400, 140, 400,137, 333);
	
		

		ctx.fill(); 
		
		// end nose -------------------------------------------------------------------------------------------------------
	
	// cap --------------------------------------------------------------------------------------------------------------------------------------------------------
	
		// BG cap
		
		grad = ctx.createRadialGradient(0,0,0,0,50,600); 
		
		
		
		grad.addColorStop(0, colorCap0);
		grad.addColorStop(1, colorCap1);
		
	
		
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(45, 255); 
	
		ctx.bezierCurveTo(12,230, 10, 160,39, 120);
		ctx.bezierCurveTo(70,50, 150,7,200, 10);
		ctx.bezierCurveTo(330,15, 360, 120,365, 126);    
		ctx.bezierCurveTo(400,200, 380,240,356, 255);
		ctx.bezierCurveTo(360,140, 240,130,200, 127);
		ctx.bezierCurveTo(160,130, 40,130,45, 255);
		ctx.fill();
		
		// End BG cap
		
		// 'M' CONTAINER 
		
		grad = ctx.createLinearGradient(0,100,5,150); 
		grad.addColorStop(0, "#ffffff");
		grad.addColorStop(1, "#cccccc");
		
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(159, 130); 
	
		ctx.bezierCurveTo(150,140, 110, 50,200, 43);
		ctx.bezierCurveTo(290,50, 250, 140,247, 130);

		ctx.fill(); 
		
		// 'M' on the cap
		
		grad = ctx.createLinearGradient(0,100,5,150);; 
		grad.addColorStop(0, colorCap0);
		grad.addColorStop(1, colorCap1);
		

		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(169, 123); 
		
		ctx.lineTo(152, 113);
		ctx.lineTo(181, 57);
		ctx.lineTo(200, 81);
		ctx.lineTo(221, 57);
		ctx.lineTo(248, 113);
		ctx.lineTo(230, 123);
		ctx.lineTo(218, 80);
		ctx.lineTo(200, 100);
		ctx.lineTo(183, 80);
		ctx.lineTo(169, 123);

		ctx.fill(); 
	
		grad = ctx.createLinearGradient(90,0,0,150);
		
		grad.addColorStop(1, colorCap0); 
		grad.addColorStop(0, colorCap1);
		
		
	
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(42, 230); 
		
		ctx.bezierCurveTo(40,180, 80, 130,200, 125);
		ctx.bezierCurveTo(310,120, 360, 205,358, 230);
		ctx.bezierCurveTo(350,180, 250, 140,200, 145);
		ctx.bezierCurveTo(40,145, 50, 280,42, 230);
		

		ctx.fill(); 
		
		grad = ctx.createLinearGradient(90,0,0,150);
		
		
		grad.addColorStop(0, colorCap3); 
		grad.addColorStop(1, colorCap4);
		
		
	
	
		ctx.fillStyle = grad;
	
		ctx.beginPath()
		ctx.moveTo(42, 235); 
		
		ctx.bezierCurveTo(40,220, 80, 140,200, 143);
		ctx.bezierCurveTo(300,140, 360, 205,358, 230);
		ctx.bezierCurveTo(350,205, 250, 165,200, 165);
		ctx.bezierCurveTo(40,170, 50, 285,42, 235);
		
		ctx.fill(); 
		
	}

setInterval(function(){
  if (i === 0) {
    drawMarioGG()     
  } else if (i === 1) {
    var ArrayCol = ['#0d59d6','#163d7d','#163d7d','#163d7d'];
    drawMarioGG (ArrayCol[0],ArrayCol[1],ArrayCol[2],ArrayCol[3]);
  } else if (i === 2) {
    ArrayCol = ['#34db0d','#248b0d','#248b0d','#248b0d'];
    drawMarioGG (ArrayCol[0],ArrayCol[1],ArrayCol[2],ArrayCol[3]);
    i = -1;
  }
	
  i++;
  
},1000)
