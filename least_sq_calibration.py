import numpy as np

def least_sq_calibration(input):
    # Filter invalid value
    input = input[~((np.isnan(input)).any(axis=1))] 
    x = input[:,0]
    y = input[:,1]
    px = input[:,2]
    py  = input[:,3]
    num_points = input.shape[0]
    # Least square estimation
    M = np.mat([
        [num_points,
            x.sum(),
            y.sum(),
            np.multiply(x,y).sum(),
            np.square(x).sum(),
            np.square(y).sum()],
        [x.sum(),
            np.square(x).sum(),
            np.multiply(x,y).sum(),
            np.multiply(np.square(x),y).sum(),
            np.power(x,3).sum(),
            np.multiply(x,np.square(y)).sum()],
        [y.sum(),
            np.multiply(x,y).sum(),
            np.square(y).sum(),
            np.multiply(x,np.square(y)).sum(),
            np.multiply(np.square(x),y).sum(),
            np.power(y,3).sum()],
        [np.multiply(x,y).sum(),
            np.multiply(np.square(x),y).sum(),
            np.multiply(x,np.square(y)).sum(),
            np.multiply(np.square(x),np.square(y)).sum(),
            np.multiply(np.power(x,3),y).sum(),
            np.multiply(x,np.power(y,3)).sum()],
        [np.square(x).sum(),
            np.power(x,3).sum(),
            np.multiply(np.square(x),y).sum(),
            np.multiply(np.power(x,3),y).sum(),
            np.power(x,4).sum(),
            np.multiply(np.square(x),np.square(y)).sum()],
        [np.square(y).sum(),
            np.multiply(x,np.square(y)).sum(),
            np.power(y,3).sum(),
            np.multiply(x,np.power(y,3)).sum(),
            np.multiply(np.square(x),np.square(y)).sum(),
            np.power(y,4).sum()]
    ])

    N_x = np.mat([
        [px.sum()],
        [np.multiply(px,x).sum()],
        [np.multiply(px,y).sum()],
        [np.multiply(px,np.multiply(x,y)).sum()],
        [np.multiply(px,np.square(x)).sum()],
        [np.multiply(px,np.square(y)).sum()]
    ])

    N_y = np.mat([
        [py.sum()],
        [np.multiply(py,x).sum()],
        [np.multiply(py,y).sum()],
        [np.multiply(py,np.multiply(x,y)).sum()],
        [np.multiply(py,np.square(x)).sum()],
        [np.multiply(py,np.square(y)).sum()]
    ])

    try:
        coeff_x = np.asarray(np.linalg.solve(M,N_x))
    except:
        coeff_x = np.asarray(np.matmul(np.linalg.pinv(M),N_x))

    try:
        coeff_y = np.asarray(np.linalg.solve(M,N_y))
    except:
        coeff_y = np.asarray(np.matmul(np.linalg.pinv(M),N_y))

    return np.hstack((coeff_x,coeff_y))