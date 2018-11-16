import logging
import netCDF4 as ncdf


def insert_soil_in_wrfinput(soilfile, wrfinput):
    soilnc = ncdf.Dataset(soilfile, "r")
    wrfinnc = ncdf.Dataset(wrfinput, "a")

    for varname in ["TSLB", "SMOIS", "SH2O", "SMCREL", "SMCREL", "SNOW","SNOWH",
                    "TSK"]:
        strparam = (varname, soilfile, wrfinput)
        logging.info("Copying variable %s from %s to %s" % strparam)
        soilnc_var = soilnc.variables[varname]
        wrfinnc_var = wrfinnc.variables[varname]
        wrfinnc_var[:] = soilnc_var[:]

    wrfinnc.sync()
    wrfinnc.close()
    soilnc.close()
