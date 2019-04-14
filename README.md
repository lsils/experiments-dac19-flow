## *Scalable Generic Logic Synthesis: One Approach to Rule Them All* (Experiments for DAC'19)

### Installation

* Install Python 3 binding (versionn 3.0a2.dev5) of `cirkit3` (https://github.com/msoeken/cirkit) with `pip`:
```
python3 -m pip install cirkit==3.0a2.dev5
```

* Clone and build `abc`: https://github.com/berkeley-abc/abc (required for combinational equivalence checking)
* Add the path to the executable of `abc` to your PATH variable

* Clone the experiments repository (this repository)
* Run the experiments using Python 3:
```
python3 run.py 
```

### Additional notes

Two parameters in the top section of `run.py` can be customized to show more/less information:

| Parameter              | Effect                                                           |
| :--------------------- | :--------------------------------------------------------------- |
| verbose = True         | Prints the statistics for each optimizing transformation         |
| print_progress = True  | Prints statistics for each benchmark (immediately when finished) |

As a final results, the script `run.py` produces the data in Table 2 in **[RienerTH+19]** in LATEX
format, i.e., the results of running `compress2rs` using AIGs, MIGs, XAGs, and additionally also
for XMGs. The columns for XMGs are not shown in the paper.

### Reference

These results are described in the paper **[RienerTH+19]**: Heinz Riener, Eleonora Testa, Winston Haaswijk,
Alan Mishchenko, Luca Amaru, Giovanni De Micheli, Mathias Soeken, *Scalable Generic Logic Synthesis: One
Approach to Rule Them All*, in *Design Automation Conference* 2019.
