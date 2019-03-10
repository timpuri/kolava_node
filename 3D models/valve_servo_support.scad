render_mount=true;
render_axel=true;

// servo mount
if(render_mount) {
    difference() {
        translate([0,10,-19]) {
            difference() {
                difference() {
                    // base
                    translate([0,0,2.5]) cube([40,115,30],center=true);
                    // servo hole
                    cube([20.5,40.5,40.5],center=true);
                }
                
                // servo mountig bolt holes
                for(multiplier=[[1,1],[-1,1],[1,-1],[-1,-1]]) {
                    translate([multiplier[0]*5,multiplier[1]*23.5]) {
                        cylinder(h=55,r1=1.5,r2=1.5,$fn= 16,center=true);
                    }
                }
            }
        }

        // inner cuttings
        translate([0,0,12]) difference() {
            cylinder(h=50,r1=40.5,r2=40.5,$fn=32,center=true);
        }
        cylinder(h=55,r1=38,r2=38,$fn=32,center=true);

        // outer cuttings
        difference() {
            cylinder(h=70,r1=80.5,r2=80.5,$fn=16,center=true);
            cylinder(h=70,r1=43.5,r2=43.5,$fn=72,center=true);
        }
        
        // base mounting holes
        for(multiplier=[-1,1]) {
               translate([0,0,-5]) rotate([-90,0,multiplier*20]) {
                    cylinder(h=155,r1=1.5,r2=1.5,$fn= 16,center=true);
                }
        }
    }
}

// axel
if(render_axel) {
    difference() {
        // axel
        union() {
            cylinder(h=77,r1=7,r2=7,$fn=32);
            translate([0,0,-10]) cylinder(h=10,r1=12,r2=12,$fn=32);
        }
        
        rotate([0,0,90]) translate([0,0,-10]) union() {
            // servo axel tightening
            translate([-1,0,0]) cube([2,20,15]);
            translate([-10,5,5]) rotate([90,0,90]) union() {
                // bolt hole
                cylinder(h=20,r1=1.55,r2=1.55,$fn=32);
                // bolt head hole
                translate([0,0,15]) cylinder(h=20,r1=3,r2=3,$fn=32);
                // nut hole
                translate([0,0,-15]) cylinder(h=20,r1=3.1,r2=3.1,$fn=8);
            }
            // servo axel hole
            cylinder(h=15,r1=3,r2=3,$fn=32);
        }
        // plate mounting
        translate([0,0,52]) {
            cube([40,1,50],center=true);
        }
        
        // plate screw holes
        for(positions=[[0,0,44],[0,0,65.5]]) {
            translate(positions) {
                rotate([-90,0,0]) {
                    // bolt hole
                    cylinder(h=55,r1=1.8,r2=1.8,$fn=16,center=true);
                    // bolt head hole
                    translate([0,0,6]) cylinder(h=3.3,r1=3.3,r2=3,$fn=16,center=true);
                    // nut hole
                    translate([0,0,-6]) cylinder(h=3.1,r1=3.1,r2=3,$fn=8,center=true);
                }
            }
        }
   }
   // position indicator
   translate([0,-10,-10]) {
       difference() {
           translate([3,0,0]) cube([45,20,3]);
           rotate([0,0,-11]) translate([-5,19,0]) cube([60,20,4]);
           rotate([0,0,11]) translate([-5,-19,0]) cube([60,20,4]);
       }
   }
}