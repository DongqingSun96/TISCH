# singleCell_gse_parser
single cell data parser from GEO 

**Clone the repository and do as follow:**
1. make sure that MySQL is isntalled in your device, and you have the account to create a new database,   
if no, install one, or contact your manager
2. install a miniconda3, then create a environment by doing:
```
conda env create -n py3_geo -f requirement.yaml
conda activate py3_geo
```
3. create a mysql database (named by yourself), and fill in the SQL file
4. revise the database name and password in in ./dc2/dc2/setting.py, using the one you just set
5. test your environment deploy, it is ok, if no error report when you run:
```
python env.py
```
6. run parser:
```
python scrna_parser_runner.py -h
```
examples can be found in run.sh file



