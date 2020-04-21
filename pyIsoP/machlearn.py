class machlearn:


    #* #     #    #     #####  #     # ### #     # #######    #       #######    #    ######  #     #
    #* ##   ##   # #   #     # #     #  #  ##    # #          #       #         # #   #     # ##    #
    #* # # # #  #   #  #       #     #  #  # #   # #          #       #        #   #  #     # # #   #
    #* #  #  # #     # #       #######  #  #  #  # #####      #       #####   #     # ######  #  #  #
    #* #     # ####### #       #     #  #  #   # # #          #       #       ####### #   #   #   # #
    #* #     # #     # #     # #     #  #  #    ## #          #       #       #     # #    #  #    ##
    #* #     # #     #  #####  #     # ### #     # #######    ####### ####### #     # #     # #     #
    """
    Contains code to train the machine learning model to predict the first shell coordination nunber using Gaussian Process Regression (GPR)
    * Features : logarithm_10 of pressure [log(P)], void fraction (VF), largest cavity dia (LCD), pore limiting dia. (PLD)
    * refer to the documentation page for the format of the training data
    
    """
    def __init__(self, scale=0.5, bounds=(0.1,10.0), restarts=10):
    
        """ 
        Initialize Gaussian Process Regression (GPR) model for predicting the first shell coordination number as a function of 
        logarithm_10 of pressure [log(P)], void fraction (VF), largest cavity dia (LCD) and  pore limiting dia. (PLD). 
        DEFAULTS: The kernel used is RationalQuadratic with length scale=0.5 with lengths bounded by (0.1,10) and 10 optimizer restarts.
        
        The choice of the kernel is based on preliminary testing. To use a differerent kernel refer to 
        https://scikit-learn.org/stable/modules/gaussian_process.html#gaussian-process-regression-gpr 
        
        to use a different method refer to:
        https://scikit-learn.org/stable/supervised_learning.html#supervised-learning

        both of which beyond the scope of this simple routine.
    
        :type scale: float
        :param scale:lengthscale hyperparameter for the RQ kernel
    
        :type bounds: float
        :param bounds:bounds to the length hyperparameter for the RQ kernel
    
        :type restarts:int 
        :param restarts: number of GPR optimizer restarts.
    
        :raises:
    
        :rtype: An instance of the machlearn class.

        """    
        from sklearn.gaussian_process.kernels import RationalQuadratic
        from sklearn.gaussian_process import GaussianProcessRegressor

        self.n1_data=[]
        self.X_tr= []
        self.y_tr=[]
        self.X_test=[]
        self.y_test=[]
        self.method ='Gaussian Process Regression'
        self.kernel_name='Rational Quadratic '
        self.length_scale=scale 
        self.bounds=bounds
        self.restarts=restarts
        self.kernel = RationalQuadratic(length_scale=self.length_scale, length_scale_bounds=self.bounds)
        self.gp = GaussianProcessRegressor(kernel=self.kernel, n_restarts_optimizer=self.restarts)

    def GPR4n1(ml_obj, data_file, train_fraction):
        
        """ 
        Quick and easy default function to train and test the Gaussian Process Regression (GPR) model for predicting the first shell coordination number as a function of 
        logarithm_10 of pressure [log(P)], void fraction (VF), largest cavity dia (LCD) and  pore limiting dia. (PLD). 
        DEFAULTS: The kernel used is RationalQuadratic with length scale=0.5 with lengths bounded by (0.1,10) and 10 optimizer restarts.
        
        The choice of the kernel is based on preliminary testing. To use a differerent kernel refer to 
        https://scikit-learn.org/stable/modules/gaussian_process.html#gaussian-process-regression-gpr 
        
        to use a different method refer to:
        https://scikit-learn.org/stable/supervised_learning.html#supervised-learning

        both of which beyond the scope of this simple routine.
        
        
        :type data_file: str
        :param data_file: The path to the text file with the training and testing data.
        File should have 5 columns corresponding to (no header line):
        logarithm_10 of pressure [log(P)], void fraction (VF), largest cavity dia (LCD), pore limiting dia. (PLD), first shell coordination number (n1)

        :type ml_obj: instacne of the machlearn class
        :param ml_obj: will be updated with the testing, training data and predictions and the Gaussian Process Regressor handle from scikit-learn.

        :type train_fraction: float
        :param train_fraction: fraction of the data to be used as the training part. Rows will be chosen randomly
    
        :raises:
    
        :rtype: An update instance of the machlearn class
        
        """    
        import pandas as pd
        import numpy as np

        ml_obj.n1_data               = pd.read_csv(data_file, delimiter=',', header=None, names=["log(P)", "Vf", "lcd", "pld", "n1"])
        msk                          = np.random.rand(len(ml_obj.n1_data)) < (1-train_fraction)
        ml_obj.X_tr, ml_obj.y_tr     = ml_obj.n1_data[~msk][['log(P)', 'Vf', 'lcd', 'pld']].values, ml_obj.n1_data[~msk][['n1']].values
        ml_obj.X_test, ml_obj.y_test = ml_obj.n1_data[msk][['log(P)', 'Vf', 'lcd', 'pld']].values, ml_obj.n1_data[msk][['n1']].values
        ml_obj.gp.fit(ml_obj.X_tr, ml_obj.y_tr)
        ml_obj.X_test, ml_obj.y_test = ml_obj.n1_data[msk][['log(P)', 'Vf', 'lcd', 'pld']].values, ml_obj.n1_data[msk][['n1']].values
        return ml_obj
