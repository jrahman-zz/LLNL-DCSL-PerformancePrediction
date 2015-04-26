#/bin/bash

LIBS="numpy scipy scikits.bootstrap scikit-learn numexpr bottleneck matplotlib statsmodels pandas seaborn seaborn"

for LIB in ${LIBS}; do
    echo "Installing ${LIB}..."
    pip install --user "${LIB}"
    if [ $? -ne 0 ]; then
        echo "Error: failed to install ${LIB}"
        exit 1
    fi
done

exit 0
