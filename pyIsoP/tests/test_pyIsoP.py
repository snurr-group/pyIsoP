"""
Unit and regression test for the pyIsoP package.

"""
# Uses the pytest fixtures decorator to take the energy grid and use it for a series of tests including
# values, writing, isotherms and etc
# Import package, test suite, and other packages as needed
import pyIsoP
import pytest
import sys

#%%
def test_pyIsoP_imported():
        """Sample test, will always pass so long as import statement worked"""
        assert "pyIsoP" in sys.modules
#%%
@pytest.fixture
def compute_grid():
        import os
        from pyIsoP import grid3D, forcefields, writer
        path_to_file = os.path.dirname(pyIsoP.__file__)+'/data/ZIF-4_mod.cif'
        t1=grid3D.grid3D(path_to_file,spacing=0.5 )
        f1=forcefields.forcefields(t1,sigma=3.95, epsilon=46,forcefield=os.path.dirname(pyIsoP.__file__)+'/../forcefield/UFF')
        t2= grid3D.grid3D.grid_calc(t1,"lj",f1)
        return t2
#%%
@pytest.fixture
def compute_grid_dask():
        import os
        from pyIsoP import grid3D, forcefields, writer
        path_to_file = os.path.dirname(pyIsoP.__file__)+'/data/ZIF-4_mod.cif'
        t1=grid3D.grid3D(path_to_file,spacing=0.5 )
        f1=forcefields.forcefields(t1,sigma=3.95, epsilon=46,forcefield=os.path.dirname(pyIsoP.__file__)+'/../forcefield/UFF')
        grid_dask= grid3D.grid3D.grid_calc_dask(t1,f1)
        t1.pot=grid_dask.compute()
        return t1       
#%%
@pytest.fixture
def compute_ml():
        import os
        import pyIsoP   
        from pyIsoP import machlearn
        print("Testing the machine learning using GPR")
        path_to_file = os.path.dirname(pyIsoP.__file__)+'/data/for_gpr_large.dat'
        ml=machlearn.machlearn(restarts=1)
        ml=machlearn.machlearn.GPR4n1(ml,path_to_file,0.1)
        return ml
#%%
@pytest.fixture
def compute_histo(compute_grid):
        from pyIsoP import histo
        h=histo.histo()
        h=histo.histo.grid2histo(compute_grid,h)
        return h
#%%
def test_grid_values(compute_grid):
        import numpy as np
        print("Testing the energy grid calculation")
        print(str(np.min(compute_grid.pot))), "Energy minimum looks good!"
        assert np.abs(np.min(np.round(compute_grid.pot, decimals=2)+1819.74)<=1E-4), "Grid minimum does not match reference"
#     assert(np.max(compute_grid.pot_repeat)==)
#%%

def test_grid_values_dask(compute_grid_dask):
        test_grid_values(compute_grid_dask)

#%%
def test_write_grid(compute_grid):
        import pyIsoP
        import os
        from pyIsoP import writer
        import numpy as np

        print("Testing the grid writer")
        path_to_out_vtk = os.path.dirname(pyIsoP.__file__)+'/data/zif-4_grid'
        path_to_out_pdb = os.path.dirname(pyIsoP.__file__)+'/data/zif-4_replicated.pdb'
        print("Writing .vts and .pdb tests into the data folder")
        writer.writer.write_vts(compute_grid,path_to_out_vtk, 1,1,1)
        writer.writer.write_frame(compute_grid,path_to_out_pdb)
        #should we assert something..?
#%%
def test_write_grid_dask(compute_grid_dask):
        test_write_grid(compute_grid_dask)

#%%
def test_histo_vals(compute_histo):
        import numpy as np
        print("Testing histogram values")
        # some check on the zif-4 energy histogram, within 1 kBT of expected
        reference_hist = np.array([-23.89147811, -23.40855962, -22.92564113, -22.44272265,
           -21.95980416, -21.47688567, -20.99396718, -20.5110487 ,
           -20.02813021, -19.54521172, -19.06229324, -18.57937475,
           -18.09645626, -17.61353777, -17.13061929, -16.6477008 ,
           -16.16478231, -15.68186382, -15.19894534, -14.71602685,
           -14.23310836, -13.75018988, -13.26727139, -12.7843529 ,
           -12.30143441, -11.81851593, -11.33559744, -10.85267895,
           -10.36976046,  -9.88684198,  -9.40392349,  -8.921005  ,
            -8.43808651,  -7.95516803,  -7.47224954,  -6.98933105,
            -6.50641257,  -6.02349408,  -5.54057559,  -5.0576571 ,
            -4.57473862,  -4.09182013,  -3.60890164,  -3.12598315,
            -2.64306467,  -2.16014618,  -1.67722769,  -1.19430921,
            -0.71139072,  -0.22847223])
        print(str(np.sum(np.abs(compute_histo.E-reference_hist))))
        assert np.sum(np.abs(compute_histo.E-reference_hist))<=0.1,"Histogram doesnot matches reference!"
#%%
def test_machlearn(compute_ml):
        print("Testing the trained ML model")
        import numpy as np
        print(str(compute_ml.gp.predict([[6,0.5,10,5]])))
        assert np.abs(compute_ml.gp.predict([[6,0.5,10,5]])-3) <=1, "Coordination number predicted doesn't agree with reference!"  # See if the predicted n1 is within a certain expected range
#%%
def test_machlearn2():

        print("Testing the trained ML model")
        import numpy as np
        import joblib
        import pyIsoP
        import os
        path_to_joblib_dump=os.path.dirname(pyIsoP.__file__)+'/data/gprmodel_pyIsoP.joblib'
        gpr = joblib.load(path_to_joblib_dump)
#        print(str(gpr.predict([[6,0.5,10,5]])))
        assert np.abs(gpr.predict([[6,0.5,10,5]])-3) <=1, "Coordination number predicted doesn't agree with reference!"  # See if the predicted n1 is within a certain expected range

#%%
def test_predictor(compute_histo, compute_ml):
        from pyIsoP import predictor
        import numpy as np
        print("Testing the isotherm prediction routine")

        n_pressures=20
        P=np.linspace(1E-5,100,n_pressures)
        T=298
        Vf=0.66
        lcd=5.1
        pld=2.4 
        X_test           = np.array([[Vf, lcd, pld],]*n_pressures)
        X_test           = np.hstack((np.reshape(np.log10(P*1E5),(n_pressures,1)), X_test))
        n1=compute_ml.gp.predict(X_test)
        refvals=np.array([[ 23.78752723],
           [ 43.53239219],
           [ 44.43192367],
           [ 44.89588641],
           [ 45.1897038 ],
           [ 45.39587854],
           [ 45.5499096 ],
           [ 45.66999489],
           [ 45.76656782],
           [ 45.84609705],
           [ 45.91283278],
           [ 45.96969572],
           [ 46.01876613],
           [ 46.06156964],
           [ 46.09925272],
           [ 46.1326949 ],
           [ 46.16258297],
           [ 46.18946154],
           [ 46.21376834],
           [ 46.23585941]])
#        h=compute_histo
       
        g_L_CH2=predictor.predictors.predict_isotherm(T,P,Vf,compute_histo,n1,epsilon=46,MA=14)
        print(g_L_CH2)
        print(refvals)
        print(str(np.sum(np.abs(g_L_CH2-refvals))))
        assert(np.sum(np.abs(g_L_CH2-refvals))<=5), "The predicted isotherm does not match the reference!"
#%%

