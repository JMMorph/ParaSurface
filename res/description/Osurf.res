CONTAINER Osurf {
    INCLUDE Obase;
    NAME Osurf;

    GROUP ID_OBJECTPROPERTIES {

        GROUP {
            DEFAULT 0;
            LAYOUTGROUP;
            COLUMNS 2;

            GROUP ID_COLA{
                LONG SURF_TYPE
                {
                    CYCLE
                    {
                        SURF_TYPE_MONKEY_SADDLE;
                        SURF_TYPE_SINE_WAVE;
                        SURF_TYPE_SPIRAL_WAVE;
                        SURF_TYPE_DINIS_SURFACE;
                        SURF_TYPE_WAVE_BALL;
                        SURF_TYPE_HYPERBOLIC_HELICOID;
                        SURF_TYPE_CROSSED_THROUGH_SURFACE;
                        -1;
                        SURF_TYPE_MOBIUS_STRIP;
                        SURF_TYPE_SINE_SURFACE;
                        SURF_TYPE_COSINE_SURFACE;
                        SURF_TYPE_SINE_CUBE;
                        SURF_TYPE_EIGHT_SURFACE;
                        SURF_TYPE_HYPERBOLIC_OCTAHEDRON;
                        SURF_TYPE_BREATHER_SURFACE;
                        SURF_TYPE_PSEUDO_CROSS_CAP;
                        SURF_TYPE_BOY_SURFACE_I;
                        SURF_TYPE_BOY_SURFACE_II;
                        SURF_TYPE_TWISTED_SPHERE;
                        SURF_TYPE_KLEIN_CYCLOID;
                        SURF_TYPE_JENNER_KLEIN_BOTTLE;
                        SURF_TYPE_STEREOGRAPHIC_SPHERE;
                        SURF_TYPE_CROSS_CAP;
                        SURF_TYPE_STROPHOID_CILINDER;
                        -1;
                        SURF_TYPE_KLEIN_BOTTLE;
                        SURF_TYPE_SEASHELL_1;
                        SURF_TYPE_SEASHELL_2;
                        SURF_TYPE_PILLOW;
                        SURF_TYPE_MILK_CARTON;
                        SURF_TYPE_SPINNING_TOP;
                        SURF_TYPE_BOWTIE;
                        SURF_TYPE_CRESCENT;
                        SURF_TYPE_LAWSON_BOTTLE;
                        SURF_TYPE_DROP_OR_EGG;
                        SURF_TYPE_APPLE_I;
                        SURF_TYPE_FRUIT;
                        SURF_TYPE_CORKSCREW;
                        SURF_TYPE_GEAR_TUBE;
                        SURF_TYPE_UMBRELLA;
                        SURF_TYPE_TUDOR_ROSE;
                        SURF_TYPE_INVOLUTE_CONOID;
                        SURF_TYPE_FISH_SURFACE;
                        -1;
                        SURF_TYPE_ASYMETRIC_TORUS;
                        SURF_TYPE_TRICUSPID_TORUS;
                        SURF_TYPE_ASTROID_TORUS;
                        SURF_TYPE_UMBILIC_TORUS;
                        SURF_TYPE_EIGHT_TORUS;
                        SURF_TYPE_TWISTED_EIGHT_TORUS;
                        SURF_TYPE_WAVE_TORUS;
                        SURF_TYPE_GEAR_WHEEL_TORUS;
                        SURF_TYPE_SPIRAL_TORUS;
                        SURF_TYPE_TORUS_KNOT;
                        SURF_TYPE_MULTI_TORUS_SHAPE;
                        SURF_TYPE_BRAIDED_TORUS;
                        SURF_TYPE_ELLIPTIC_TORUS;
                        -1;
                        SURF_TYPE_CUSTOM;

                    }
                }
            }

            GROUP ID_COLB{
                BUTTON SURF_RESET { }
            }
        }



        GROUP ID_BASIC_PROPERTIES {
            DEFAULT 1;
            LAYOUTGROUP;
            COLUMNS 2;

            GROUP {

                LONG SURF_ORIENTATION {
                    CYCLE
                    {
                        SURF_ORIENTATION_XP;
                        SURF_ORIENTATION_XN;
                        SURF_ORIENTATION_YP;
                        SURF_ORIENTATION_YN;
                        SURF_ORIENTATION_ZP;
                        SURF_ORIENTATION_ZN;
                        
                    }
                }

                LONG SURF_U_SEGMENTS { MIN 1; STEP 1; }
                REAL SURF_U_MIN { STEP 0.1; }
                REAL SURF_U_MAX { STEP 0.1; }
                REAL SURF_U_PERCENT { UNIT PERCENT; MIN 0; MAX 100; STEP 1; }
                REAL SURF_U_OFFSET { UNIT DEGREE; STEP 1; }
                BOOL SURF_WELD { }
            }

            GROUP {
                
                REAL SURF_SCALE { STEP 1; }
                LONG SURF_V_SEGMENTS { MIN 1; STEP 1; }
                REAL SURF_V_MIN { STEP 0.1; }
                REAL SURF_V_MAX { STEP 0.1; }
                REAL SURF_V_PERCENT { UNIT PERCENT; MIN 0; MAX 100; STEP 1; }
                REAL SURF_V_OFFSET { UNIT DEGREE; STEP 1; }
                BOOL SURF_UPDATE_UVW { }
            }


        }

        GROUP ID_COEFFICIENTS {
            DEFAULT 1;
            STATICTEXT SURF_NUMBER_COEFFICIENTS {  }
            REAL SURF_COEFFICIENT_A { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_B { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_C { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_D { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_F { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_G { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_H { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_I { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_J { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_K { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER; }
            REAL SURF_COEFFICIENT_L { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_M { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_N { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_O { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_P { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_Q { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_R { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_S { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            REAL SURF_COEFFICIENT_T { MIN -999999; MAX 999999; STEP 0.1; MINSLIDER 0; MAXSLIDER 20; CUSTOMGUI REALSLIDER;}
            
        }

        GROUP ID_CUSTOM_SURFACE {
            DEFAULT 0;
            STRING SURF_CUSTOM_X { ANIM OFF; CUSTOMGUI MULTISTRING;}
            STRING SURF_CUSTOM_Y { ANIM OFF; CUSTOMGUI MULTISTRING;}
            STRING SURF_CUSTOM_Z { ANIM OFF; CUSTOMGUI MULTISTRING;}
            STRING SURF_CUSTOM_AUX { ANIM OFF; CUSTOMGUI MULTISTRING;}
        }


        GROUP ID_RATIO {
            DEFAULT 0;
            LAYOUTGROUP;
            COLUMNS 3;

            GROUP {
                REAL SURF_ASPECT_RATIO_X { STEP 0.1; }
                REAL SURF_GRID_X { UNIT PERCENT; MIN 0; MAX 100; STEP 1; MINSLIDER 1; MAXSLIDER 200; }
            }

            GROUP {
                REAL SURF_ASPECT_RATIO_Y { STEP 0.1; }
                REAL SURF_GRID_Y { UNIT PERCENT; MIN 0; MAX 100; STEP 1; MINSLIDER 1; MAXSLIDER 200; }
            }

            GROUP {
                REAL SURF_ASPECT_RATIO_Z { STEP 0.1; }
                REAL SURF_GRID_Z { UNIT PERCENT; MIN 0; MAX 100; STEP 1; MINSLIDER 1; MAXSLIDER 200; }
            }
        
        }

        GROUP ID_SURFACE_INFO {
            DEFAULT 0;
            STATICTEXT SURF_SURFACE_NAME { }
            STATICTEXT SURF_SURFACE_COEFFICIENTS { }
            STRING SURF_SURFACE_EQUATIONS { ANIM OFF; CUSTOMGUI MULTISTRING; SCALE_V; WORDWRAP; READONLY; }
        }

        
    }
}