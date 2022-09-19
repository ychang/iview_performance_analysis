Welcome to IVIEW+ Performance Analysis Tool!

Author : Yong Jun Chang (yongjun.chang@hotmail.com)

Installation:

pip install -r requirements.txt

Options:

-i --input  : Source directory of inference output (jpg and txt)
-o --output : Output directory of analysis results
-c --cs     : Source path of cofidence score file corresponding to the input
--mode      : {interactive, batch} 

Example:

python iview_performance_analysis.py -i ./data/france -o ./output_france -c ./data/image_france_cs.txt
python iview_performance_analysis.py --batch -i ./data/france -o ./output_france -c ./data/image_france_cs.txt

Source code can be found from the GITHUB in:

    git://github.com/ychang/iview_performance_analysis.git

