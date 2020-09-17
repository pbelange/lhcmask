def measure_coupling(mad):

    assert mad.globals.mylhcbeam>=1

    mad.input('''
    if(mylhcbeam==1)
    {kqtf=kqtf.b1;kqtf0=kqtf.b1;
     kqtd=kqtd.b1;kqtd0=kqtd.b1;
     kqtf.b1:=kqtf;
     kqtd.b1:=kqtd;};

    if(mylhcbeam > 1)
    {kqtf=kqtf.b2;kqtf0=kqtf.b2;
     kqtd=kqtd.b2;kqtd0=kqtd.b2;
     kqtf.b2:=kqtf;
     kqtd.b2:=kqtd;};

    ! closest tune
    qmid=(qx0-qx00+qy0-qy00)*0.5;

    match;
    global, q1=qx00+qmid,q2=qy00+qmid;
    vary,   name=kqtf, step=1.E-9;
    vary,   name=kqtd, step=1.E-9;
    lmdif,  calls=50, tolerance=1.E-10;
    endmatch;

    ! Quick minimization based on linear machine
    cmrskew0 = cmrskew;
    cmiskew0 = cmiskew;
    twiss; qx=table(summ,q1); qy=table(summ,q2);
    cta0     = abs(2*(qx-qy)-round(2*(qx-qy)))/2;
    closest0 = cta0;
    !value,closest0;

    if(mylhcbeam==1)
    {kqtf.b1=kqtf0;
    kqtd.b1=kqtd0;};

    if(mylhcbeam > 1)
    {kqtf.b2=kqtf0;
     kqtd.b2=kqtd0;};
    ''')

    return mad.globals.cta0

