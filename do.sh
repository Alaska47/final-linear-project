rm -rf output*.png

convert IMG*.JPG -rotate 90 -resize 75% output.png
rm -rf IMG*.JPG

python lin_proj.py output.png output_1_IDENTITY.png identity 1
python lin_proj.py output.png output_2_SHARPEN.png sharpen 1
python lin_proj.py output.png output_3_BLUR.png blur 3
python lin_proj.py output.png output_4_BOTTOM_EDGE.png bottom_edge 1
python lin_proj.py output.png output_5_TOP_EDGE.png top_edge 1
python lin_proj.py output.png output_6_LEFT_EDGE.png left_edge 1
python lin_proj.py output.png output_7_RIGHT_EDGE.png right_edge 1
python lin_proj.py output.png output_8_EMBOSS.png emboss 1

git add output*

git commit -m "add example"

git push origin master

rm -rf output.png
