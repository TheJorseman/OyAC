from csv import reader
from math import log2,ceil

def open_csv(filename):
    csv = reader(open(filename))
    return [row for row in csv]

def extract_row_data(rows,limits):
    return rows[limits[0]-1:limits[1]]

def extract_colum_data(rows,first_indx, second_indx):
    return [row[first_indx:second_indx] for row in rows]

def extract_dir_content(rows,dir_range,content_range):
    data = {}
    for row in rows:
        rom_dir = "".join(row[dir_range[0]:dir_range[1]])
        rom_content = "".join(row[content_range[0]:content_range[1]])
        data[rom_dir] = rom_content
    return data

def create_mif_file(rom,width,depth,output_name):
    template = open("mif_template.mif")
    mif = ""
    for line in template:
        mif += line
    mif = mif.replace("{WIDTH}",str(width))
    mif = mif.replace("{DEPTH}",str(depth))
    data_str = ""
    data_format = "\t{rom_dir}  :   {data};\n"
    dir_length = int(log2(depth) + 1)
    for rom_dir,data in rom.items():
        data_str += data_format.format(rom_dir=rom_dir.zfill(dir_length)  ,data=str(data))
    if len(rom) < depth:
        default = "".zfill(width)
        rem_0 = str(bin(len(rom))).replace("0b","").zfill(dir_length)
        rem_1 = str(bin(depth - 1)).replace("0b","").zfill(dir_length)
        data_str += "\t[{ini}..{end}]  :   {default};\n".format(ini=rem_0,end=rem_1,default=default)
    mif = mif.replace("{data}",str(data_str))
    output = open(output_name + ".mif","w")
    output.write(mif)

def main():
    # Modificable data ##############################
    # Rango de columnas donde se encuentran los datos, asi como aparece en el excel
    row_range = (3,42)
    # Rango donde se encuentra la direccion, se agrega el + 1 para darle acceso correcto a la lista 
    # Se inicia contando desde 0. 
    dir_range = (0,5 + 1)
    data_range = (6,14 + 1)
    width = 9
    depth = 64
    # Archivo de entrada
    filename = "P3.csv"
    # Nombre del archivo salida sin extension
    output_name = "rom_content" 
    ###############################################
    rows = open_csv(filename)
    data = extract_row_data(rows,row_range)
    rom = extract_dir_content(data,(0,6),(6,15))
    # Se puede calcular el valor depth
    # Utilizando un valor potencia de 2
    # depth_calc = 2 ** ceil(log2(len(rom)))
    # O simplemente con la longitud de nuestos valores
    # depth_calc = len(rom)
    ###################################################
    # Igual se puede calcular el parametro width
    # width = len(rom[0])
    rom_sorted = sorted(rom.items(),key=lambda x: int(x[0],2))
    rom_sorted = {rom_s[0]: rom_s[1] for rom_s in rom_sorted }
    create_mif_file(rom_sorted,width,depth,output_name)

if __name__ == "__main__":
    main()


