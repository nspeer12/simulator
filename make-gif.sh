#!/bin/bash

convert -delay 10 -loop 5 -dispose previous imgs/*.png render.gif
