rm -rf output*.png

convert IMG*.JPG -rotate 90 output.png
rm -rf IMG*.JPG

python lin_proj.py output.png output_1.png identity 1
python lin_proj.py output.png output_2.png sharpen 1
python lin_proj.py output.png output_3.png blur 5
python lin_proj.py output.png output_4.png edge 1

rm -rf output.png
