lightsout4=[[1, 1, 1, 0, 0, 0, 1, 0, 0],[1, 0, 1, 0, 0, 0, 1, 1, 0],[1, 0, 1, 1, 1, 1, 0, 0, 1] ,[1, 0, 0, 0, 0, 0, 1, 0, 0]]
def week2b_ans_func(lightsout4):
########## QRAM 
    qram=QuantumCircuit(11, name='qram')
    for index, j in enumerate(lightsout4[0]):
        if j==1:
            qram.ccx(0,1,index+2)
    qram.x(0)
    for index, j in enumerate(lightsout4[1]):
        if j==1:
            qram.ccx(0,1,index+2)
    qram.x(0)
    qram.x(1)
    for index, j in enumerate(lightsout4[2]):
        if j==1:
            qram.ccx(0,1,index+2)
    qram.x(1)
    qram.x([0,1])
    for index, j in enumerate(lightsout4[3]):
        if j==1:
            qram.ccx(0,1,index+2)
    qram.x([0,1])
    qram_gate=qram.to_gate()
    qram_dagger=qram_gate.inverse()
    # qc.append(qram_gate, [*range(11)])
    # qc.append(qram_dagger, [*range(11)])
    ################################################################################################
    ########### U2a
    u2a=QuantumCircuit(19, name='u2a')
    for i in range(17):
        u2a.cx(9, [0,1,3])
        u2a.cx(10, [0,1,2,4])
        u2a.cx(11, [1,2,5])
        u2a.cx(12, [0,3,4,6])
        u2a.cx(13, [1,3,4,5,7])
        u2a.cx(14, [2,4,5,8])
        u2a.cx(15, [3,6,7])
        u2a.cx(16, [4,6,7,8])
        u2a.cx(17, [5,7,8])
        u2a.x([0,1,2,3,4,5,6,7,8])
        u2a.mct([0,1,2,3,4,5,6,7,8], 18)
        u2a.x([0,1,2,3,4,5,6,7,8])
        u2a.cx(17, [5,7,8])
        u2a.cx(16, [4,6,7,8])
        u2a.cx(15, [3,6,7])
        u2a.cx(14, [2,4,5,8])
        u2a.cx(13, [1,3,4,5,7])
        u2a.cx(12, [0,3,4,6])
        u2a.cx(11, [1,2,5])
        u2a.cx(10, [0,1,2,4])
        u2a.cx(9, [0,1,3])
        #####Diffuser
        #u2a.barrier()
        u2a.h([9,10,11,12,13,14,15,16,17])
        u2a.x([9,10,11,12,13,14,15,16,17])
        u2a.h(17)
        u2a.mct([9,10,11,12,13,14,15,16], 17)
        u2a.h(17)
        u2a.x([9,10,11,12,13,14,15,16,17])
        u2a.h([9,10,11,12,13,14,15,16,17])
    u2a_gate=u2a.to_gate()
    u2a_dagger=u2a_gate.inverse()
    # qc.append(u2a_gate, [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    # qc.append(u2a_dagger, [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    ##################################################################################################
    ####### Counter
    counter=QuantumCircuit(14)
    flip=[0,1,2,3,4,5,6,7,8]
    auxiliary=[10,11,12,13]
    for i in range(len(flip)):
        counter.mct([flip[i], auxiliary[0], auxiliary[1], auxiliary[2]], auxiliary[3], mode ='noancilla')
        counter.mct([flip[i], auxiliary[0], auxiliary[1]], auxiliary[2], mode ='noancilla')
        counter.ccx(flip[i], auxiliary[0], auxiliary[1])
        counter.cx(flip[i], auxiliary[0])
    counter_gate=counter.to_gate()
    counter_dagger=counter_gate.inverse()
    # qc.append(counter_gate, [*range(11,22)])
    # qc.append(counter_dagger, [*range(11,22)])
    ####################################################################################
    ### Phase
    phase=QuantumCircuit(3)
    phase.x([0,1])
    phase.ccx(0,1,2)
    phase.x([0,1])
    phase_gate=phase.to_gate()
    # qc.append(phase_gate,[23,24,25])
    #############################################################################
    qc=QuantumCircuit(26,2)
    ######## Prepare
    qc.x([20,25])
    qc.h([0,1,11,12,13,14,15,16,17,18,19,20,25])
    qc.barrier()
    #########################################################################################
    qc.append(qram_gate, [*range(11)])
    qc.barrier()
    qc.append(u2a_gate, [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    qc.barrier()
    qc.append(counter_gate, [*range(11,25)])
    qc.barrier()
    qc.append(phase_gate,[23,24,25])
    qc.barrier()
    qc.append(counter_dagger, [*range(11,25)])
    qc.barrier()
    qc.append(u2a_dagger, [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
    qc.barrier()
    qc.append(qram_dagger, [*range(11)])
    qc.barrier()
    #########################################################################################
    ######## Diffuser
    qc.h([0,1])
    qc.x([0,1])
    qc.cz(0,1)
    qc.x([0,1])
    qc.h([0,1])
    ####### Measure
    qc.measure([0,1], [0,1])
    qc=qc.reverse_bits()
    return qc