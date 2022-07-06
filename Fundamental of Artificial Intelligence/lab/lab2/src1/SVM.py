import numpy as np
# import cvxpy
import logging
import cvxopt


# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# )


class SupportVectorMachine():
    def __init__(self, C=1, kernel='Linear', epsilon=1e-4):
        self.C = C
        self.epsilon = epsilon
        self.kernel = kernel

        # Hint: 你可以在训练后保存这些参数用于预测
        # SV即Support Vector，表示支持向量，SV_alpha为优化问题解出的alpha值，
        # SV_label表示支持向量样本的标签。
        self.SV = None
        self.SV_alpha = None
        self.SV_label = None
        self.b = 0

    def KERNEL(self, x1, x2, d=2, sigma=1):
        # d for Poly, sigma for Gauss
        if self.kernel == 'Gauss':
            K = np.exp(-(np.sum((x1 - x2) ** 2)) / (2 * sigma ** 2))
        elif self.kernel == 'Linear':
            K = np.dot(x1, x2)
        elif self.kernel == 'Poly':
            K = (np.dot(x1, x2) + 1) ** d
        else:
            raise NotImplementedError()
        return K

    def fit(self, train_data, train_label):
        '''
        TODO：实现软间隔SVM训练算法
        train_data：训练数据，是(N, 7)的numpy二维数组，每一行为一个样本
        train_label：训练数据标签，是(N,)的numpy数组，和train_data按行对应
        '''
        num_samples = train_data.shape[0]
        # init kernel matrix
        kernel_matrix = np.zeros((num_samples, num_samples))
        for i in range(num_samples):
            for j in range(num_samples):
                kernel_matrix[i, j] = self.KERNEL(train_data[i], train_data[j])
        # use cvxopt.solvers.qp to solve quadratic question
        # https://cvxopt.org/userguide/coneprog.html#quadratic-programming
        # the quadratic question: the dual of the optimization problem
        # the x is for the alpha
        logging.debug(f"train_label.shape: {train_label.shape}")
        P = cvxopt.matrix(np.outer(train_label, train_label) * kernel_matrix, tc='d')
        q = cvxopt.matrix(np.ones(num_samples) * -1)
        A = cvxopt.matrix(train_label, (1, num_samples), tc='d')
        b = cvxopt.matrix(0, tc='d')
        G = cvxopt.matrix(np.concatenate((np.identity(num_samples) * -1, np.identity(num_samples)), axis=0))
        h = cvxopt.matrix(np.concatenate((np.zeros(num_samples), np.ones(num_samples) * self.C), axis=0))
        cvxopt.solvers.options['show_progress'] = False
        minimization = cvxopt.solvers.qp(P, q, G, h, A, b)
        x = np.ravel(minimization['x'])
        logging.debug(f"type(minimization): {type(minimization)}")
        logging.debug(f"type(minimization['x']): {type(minimization['x'])}")
        logging.debug(f"type(x): {type(x)}")
        logging.debug(f"x.shape: {x.shape}")
        sv_idx = x > self.epsilon
        self.SV = train_data[sv_idx]
        self.SV_label = train_label[sv_idx]
        self.SV_alpha = x[sv_idx]
        logging.debug(f"type(self.SV_alpha): {type(self.SV_alpha)}")
        logging.debug(f"self.SV_alpha.shape: {self.SV_alpha.shape}")
        self.b = self.SV_label[0]
        # for i, alpha_i in enumerate(self.SV_alpha):
        #     self.b -= alpha_i * self.SV_label[i] * self.KERNEL(self.SV[i], self.SV[0])
        tmp_matrix = np.zeros((self.SV_alpha.shape[0], self.SV_alpha.shape[0]), dtype=np.float64)
        for i, sv in enumerate(self.SV):
            tmp_matrix[i][i] = self.KERNEL(sv, self.SV[0])
        self.b -= np.matmul(
            np.matmul(
                self.SV_alpha,
                tmp_matrix,
            ),
            self.SV_label
        )

    def predict(self, test_data):
        '''
        TODO：实现软间隔SVM预测算法
        train_data：测试数据，是(M, 7)的numpy二维数组，每一行为一个样本
        必须返回一个(M,)的numpy数组，对应每个输入预测的标签，取值为1或-1表示正负例
        '''
        predictions = []
        for data in test_data:
            tmp_matrix = np.zeros((self.SV_alpha.shape[0], self.SV_alpha.shape[0]))
            for i, sv in enumerate(self.SV):
                tmp_matrix[i][i] = self.KERNEL(sv, data)
            prediction = np.matmul(
                np.matmul(
                    self.SV_alpha,
                    tmp_matrix,
                ),
                self.SV_label
            ) + self.b
            predictions.append(np.sign(prediction))
        return np.asarray(predictions)
