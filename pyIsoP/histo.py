class histo:
    
    #*####### #     # ####### ######   #####  #     #    #     # ###  #####  ####### #######  #####  ######     #    #     #
    #*#       ##    # #       #     # #     #  #   #     #     #  #  #     #    #    #     # #     # #     #   # #   ##   ##
    #*#       # #   # #       #     # #         # #      #     #  #  #          #    #     # #       #     #  #   #  # # # #
    #*#####   #  #  # #####   ######  #  ####    #       #######  #   #####     #    #     # #  #### ######  #     # #  #  #
    #*#       #   # # #       #   #   #     #    #       #     #  #        #    #    #     # #     # #   #   ####### #     #
    #*#       #    ## #       #    #  #     #    #       #     #  #  #     #    #    #     # #     # #    #  #     # #     #
    #*####### #     # ####### #     #  #####     #       #     # ###  #####     #    #######  #####  #     # #     # #     #
    """
    * Functions to calculate or read the energy histogram of amaterial
    
    """


    def __init__(self, nbins=50, E_max=1, normed_flag=True):
        """ 
        Initializes the histogram object to store the energy histogram, unit of [K] for the energy.

        :type number: int
        :param number: number of bins
    
        :type E: array of floats
        :param E: Energy of each bin in the histogram-- bincenters
    
        :type RhoE: array of floats
        :param RhoE: Normalized energy density, (area under the curve =1)

        :type E_max: float
        :param E: Maximum energy where the histogram is cut off. in units of [K]
        * DEFAULT: 10 [K], doesn't change the isotherm from prior testing
    

        :raises:
    
        :rtype: Instance of the histogram class
        
        """

        self.nbins                                                    = nbins
        self.E                                                        = []
        self.RhoE                                                     = []
        self.E_max                                                    = E_max
        self.normed_flag                                              = normed_flag
        self.name                                                     = ''

    # * Calculate histogram from PyIsoP grid object
    def grid2histo(grid_obj, hist_obj):
        """ 
        Calculate histogram from PyIsoP grid object 

        :type grid_obj: An instance of the grid3D class
        :param grid_obj: Contains energy info on a 3D grid
    
        :type hist_obj: An instance of the histo class
        :param hist_obj: Will be modified and overwritten with energy and density of sites info

        :raises:
    
        :rtype: Modified histogram object with E and RhoE.
        
        """
        import numpy as np

        hist_obj.name                                                 = grid_obj.file
        e_vals                                                        = np.reshape(grid_obj.pot, (grid_obj.nx*grid_obj.ny*grid_obj.nz, 1), order='C')
        e_vals  = e_vals/grid_obj.Temperature # Reduced units for energy
        e_vals = e_vals[~np.isnan(e_vals)]
        bins1                                                         = np.linspace(min(e_vals)-0.5, hist_obj.E_max/grid_obj.Temperature , hist_obj.nbins+1)
        # bins1 = np.reshape(bins1, (1,hist_obj.nbins+1))
        hist_obj.RhoE, binedges1 = np.histogram(e_vals, bins=bins1, density=hist_obj.normed_flag)
        bincenters                                                    = 0.5 * (binedges1[1:] + binedges1[:-1])  # Bincenters
        hist_obj.E                                                    = bincenters
        return hist_obj

     # * Calculate histogram from PyIsoP grid object
    def gridtotal2histo(grid_obj, hist_obj):
        """ 
        Calculate histogram from PyIsoP grid object using the total energy (bead + sphere sampling + disc sampling)

        :type grid_obj: An instance of the grid3D class
        :param grid_obj: Contains energy info on a 3D grid
    
        :type hist_obj: An instance of the histo class
        :param hist_obj: Will be modified and overwritten with energy and density of sites info

        :raises:
    
        :rtype: Modified histogram object with E and RhoE.
        
        """
        import numpy as np
        
        hist_obj.name = grid_obj.file
        
        e_vals = np.reshape(grid_obj.pot_total, (grid_obj.N_grid_total, 1), order='C')
        e_vals = e_vals/grid_obj.Temperature  # Reduced units for energy
        e_vals = e_vals[~np.isnan(e_vals)]
        bins1 = np.linspace(min(e_vals)-0.5, hist_obj.E_max/grid_obj.Temperature , hist_obj.nbins+1)
        # bins1 = np.reshape(bins1, (1,hist_obj.nbins+1))
        # e_vals = e_vals[~np.isnan(e_vals)]
        hist_obj.RhoE, binedges1 = np.histogram(e_vals, bins=bins1,  density=hist_obj.normed_flag)
        bincenters = 0.5 * (binedges1[1:] + binedges1[:-1])  # Bincenters
        hist_obj.E = bincenters
        return hist_obj


    # * Calculate histogtram from the RASPA generated grid file, Ben Bucior's version
    def raspa2histo(grid_filename, hist_obj):
        """ 
        Calculate histogtram from the RASPA generated grid file, Ben Bucior's version
        find it here: 

        :type grid_file:str
        :param grid_file: Path to the grid file generated by RASPA. Grid file format x y z energy dE/dx dE/dy dE/dz.  

        :type hist_obj: instance of the histo class. 
        :param hist_obj: contains all the info regarding the energy distribution of sites for a given material.  

        :raises: One has to initialize the histogram object before calling this function
        shouldn't raise any error if the .grid file is from the RASPA version published along with PyIsoP   
        which is x y z E dEx dEy dEz (last three optional), no header lines.

        :rtype: histogram object with the energies and their densities updated

        """
        import numpy as np
        import pandas as pd

        grid                                                          = pd.read_csv(grid_filename, header=None, delim_whitespace=True)  # Read the energy data
        e_vals                                                        = pd.to_numeric(grid[3][grid[3].as_matrix() != '?'])
        e_vals = e_vals/grid_obj.Temperature  # Reduced units for energy
        e_vals = e_vals[~np.isnan(e_vals)]
        bins1                                                         = np.linspace(min(e_vals)-0.5, hist_obj.E_max/grid_obj.Temperature , hist_obj.nbins+1)
        hist_obj.RhoE, binedges1 = np.histogram(e_vals, bins=bins1, density=hist_obj.normed_flag)
        bincenters                                                    = 0.5 * (binedges1[1:] + binedges1[:-1])  # Bincenters
        hist_obj.E                                                    = bincenters

        return hist_obj

    # * Read the histogram in from a file with no header and two columns
    def file2histo(histo_filename, hist_obj):
        """ 

        Read the histogram in from a file with no header and two columns 

        :type histo_filename: str   
        :param histo_filename: path to the histogram text file with two columns, keep the energy dimensionless to avoid confusion.
    
        :type hist_obj: instance of the histo class
        :param hist_obj: contains all the info regarding the energy histogram of sites for a given material  
    
        :raises: One has to initialize the histogram object before calling this function.
        pandas could throw up if the file is not formatted correctly. Refer examples section in the documentation.
    
        :rtype: histogram object with the energies and their densities updated

        """

        import pandas as pd
        import numpy as np

        histo_temp                                                    = pd.read_csv(histo_filename, header=None, delim_whitespace=True)  # Read the energy data
        hist_obj.E                                                    = np.array(histo_temp[0])
        hist_obj.RhoE                                                 = np.array(histo_temp[1])
        hist_obj.name                                                = histo_filename
        hist_obj.nbins                                               = len(hist_obj.E)  # Number of bins is dictated by the row in the histogram text file

        return hist_obj

    # * Convert cube file to histogram, .cube file maybe generated using Prof. Cory Simon's code.
    def cube2histo(cube_filename, hist_obj):
        """ 
        Convert cube file to histogram, .cube file maybe generated using Prof. Cory Simon's code in Julia.

        :type cube_filename: str
        :param cube_filename: path to the cube file generated by Prof. Cory Simon's code

        :type hist_obj: instance of the histo class
        :param hist_obj: contains all the info regarding the energy histogram of sites for a given material  

        :raises: One has to initialize the histogram object before calling this function.
        pandas could throw up if the file is not formatted correctly. Refer documentation page

        :rtype: instance of the histo class.

        """
        import pandas as pd
        import numpy as np
        from ase.io import read, write
        from ase.io.cube import read_cube_data

        data, atoms = read_cube_data(cube_filename)
        e_vals = np.reshape(data, (data.size, 1), order='C')
        e_vals = e_vals/grid_obj.Temperature  # Reduced units for energy
        e_vals = e_vals[~np.isnan(e_vals)]
        bins1 = np.linspace(min(e_vals)-0.5, hist_obj.E_max/grid_obj.Temperature , hist_obj.nbins+1)
        hist_obj.RhoE, binedges1 = np.histogram(e_vals, bins=bins1, density=hist_obj.normed_flag)
        bincenters = 0.5 * (binedges1[1:] + binedges1[:-1])  # Bincenters
        hist_obj.E = bincenters

        return hist_obj
