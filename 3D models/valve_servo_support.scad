render_mount=true;
render_axel=true;

// servo mount
if(render_mount) {
    translate([0,0,13]) difference() {
        translate([0,10,-19]) {
            difference() {
                difference() {
                    // base
                    translate([0,0,0.5]) cube([40,115,30],center=true);
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
        translate([0,0,-2]) cylinder(h=55,r1=38,r2=38,$fn=32,center=true);

        // outer cuttings
        difference() {
            cylinder(h=70,r1=80.5,r2=80.5,$fn=16,center=true);
            cylinder(h=70,r1=43.5,r2=43.5,$fn=72,center=true);
        }
        
        // base mounting holes
        for(multiplier=[-1,1]) {
               translate([0,0,-8]) rotate([-90,0,multiplier*20]) {
                    cylinder(h=155,r1=1.5,r2=1.5,$fn= 16,center=true);
                }
        }
    }
}

// axel
module axel(direct_axel_mount=true) {
    if(render_axel) {
        difference() {
            // axel
            union() {
                cylinder(h=77,r1=7,r2=7,$fn=32);
                if(direct_axel_mount) {
                    translate([0,0,-10]) cylinder(h=10,r1=12,r2=12,$fn=32);
                } else {
                    translate([0,0,-4]) cylinder(h=4,r1=12,r2=12,$fn=32);
                }
                
            }
            
            rotate([0,0,90]) translate([0,0,-10]) union() {
                if(direct_axel_mount) {
                    // servo axel tightening
                    translate([-1,0,0]) cube([2,20,15]);
                    translate([-10,5,5]) rotate([90,0,90]) union() {
                        // bolt hole
                        cylinder(h=20,r1=1.55,r2=1.55,$fn=32);
                        // bolt head hole
                        translate([0,0,17]) cylinder(h=20,r1=3,r2=3,$fn=32);
                        // nut hole
                        translate([0,0,-17]) cylinder(h=20,r1=3.1,r2=3.1,$fn=8);
                    }
                    // servo axel hole
                    cylinder(h=15,r1=3,r2=3,$fn=32);
                } else {
                    // servo circle screw mount
                    cylinder(h=15,r1=4.5,r2=4.5,$fn=32);
                    for(rotate_z=[90,180,270,360]) {
                        rotate([0,0,rotate_z]) translate([7.5,0,0]) cylinder(h=8,r1=0.75,r2=0.75,$fn=32);
                    }

                }
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
       indicator_translate = direct_axel_mount ? [0,-10,-10] : [0,-10,-4];
       translate(indicator_translate) {
           difference() {
               translate([9,0,0]) cube([39,20,3]);
               rotate([0,0,-11]) translate([-5,19,0]) cube([60,20,4]);
               rotate([0,0,11]) translate([-5,-19,0]) cube([60,20,4]);
           }
       }
    }
}

axel(true);
translate([80,0,0]) axel(false);