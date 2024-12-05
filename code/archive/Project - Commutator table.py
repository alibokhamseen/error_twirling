import numpy as np


def pauli() -> dict:
    I = np.array([[1, 0], [0, 1]], dtype=np.complex128)
    X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
    Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    return {"I": I, "X": X, "Y": Y, "Z": Z}

# print(pauli()["I"], pauli()["X"])

input1="XZ" #will be some like XYYZ
input2="XYZ"

def com(input1,input2):
    """
    Recursive function that will return the commutivity or anti-commutivity of the Pauli Gates 
    """
    #here should be the base case - shou
    ##ask ali if it should be a geenral input length case or if we can have it fixed so that input 1 size = 1
    if len(input1) == len(input2) == 1:
        AB = np.matmul(pauli()[input1],pauli()[input2])
        BA = np.matmul(pauli()[input2],pauli()[input1])
        if (AB == BA).all():
            return 1
        else:
            return -1 #ask if, say, xy=-yx like if that's just true 
    else:
        ##This should really take the string and break it up
        "shii might just make another if else branch if either of the inputs has length 1 but do i have to do it with both? "
        print("yeah we in else")
        # print(input1,input2)
        # print(input1[0],input2[0])
        for i in range(len(input1)):
            if len(input2)<1 or len(input1) == 1:
                break
            else:
                print(input1,input2)
                splitI1,splitI2 = input1[i],input2[0] 
                print(splitI1,splitI2)

                AB = np.matmul(pauli()[splitI1],pauli()[splitI2])
                BA = np.matmul(pauli()[splitI2],pauli()[splitI1])
                if (AB == BA).all():
                    return com(input1, input2[1:])
                else:
                    return (-1)*com(input1, input2[1:])


        # for i in range(len(input1)):
        #     for j in range(len(input2)):
        #         splitI1, splitI2 = input1, input2
        #         splitI1,splitI2 = splitI1[i],splitI2[j] 
        #         """
        #         yeah this is where we fuckin uuuuup.  I need to /distribute/ the terms
        #         how to do that ??? might need to make a copy but keep the other one there?  ?? 
        #         """
        #         ##recursive still??? what hthe fucck 
        #         ##maybe for i in input 1: return split1i, splitI2[1:]??
        #         AB = np.matmul(pauli()[splitI1[i]],pauli()[splitI2[j]])
        #         BA = np.matmul(pauli()[splitI2[j]],pauli()[splitI1[i]])
        #         if (AB == BA).all():
        #             return com(splitI1[1:], splitI2[1:])
        #         else:
        #             return (-1)*com(splitI1[1:], splitI2[1:])
        #         #here should be the comm of the breaking down. 
        

print(com(input1,input2))

# # print(input1[0])
# splitI1, splitI2 =input1[0], input2[0]
# print(splitI1,splitI2)
# X = np.array([[0, 1], [1, 0]],)
# Y = np.array([[0, -1j], [1j, 0]])

# print(np.matmul(X,Y))
# print(com(input1,input2))


# I = np.array([[1, 0], [0, 1]], dtype=np.complex128)
# X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
# Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
# Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

# D={"I":I,"X":X,"Y":Y,"Z":Z}

# print(np.matmul(D["X"],D["Y"]))
# class CommutatoXrTable:
#     """
#     The commmutator function Zeta takes in Pauli matrices and will return
#     a 1 if they commute or a -1 if they anticommute.
    
#     """
#     def __init__(self,gate1, gate2):
#         self.gate1 = gate1
#         self.gate2 = gate2

#     def commutation(self,gate1,gate2, **kawrgs):
#         AB = np.matmul(self.gate1, self.gate2)
#         BA = np.matmul(self.gate1, self.gate2)
#         if AB == BA:
#             return 1
