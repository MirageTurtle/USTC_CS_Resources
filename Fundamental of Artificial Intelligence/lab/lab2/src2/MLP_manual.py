import torch
import numpy as np
from matplotlib import pyplot as plt
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
)


class MLP:
    def __init__(
        self,
        layer_sizes=[10, 10, 8, 8, 4],
    ):
        # layer size = [10, 8, 8, 4]
        # 初始化所需参数
        self.layer_sizes = layer_sizes

        def softmax_cross_entropy(preds, labels):
            scores = np.exp(preds - np.max(preds, axis=1, keepdims=True))
            scores /= np.sum(scores, axis=1, keepdims=True)
            positive_scores = scores[np.arange(labels.shape[0]), labels]
            # logging.debug(f"positive_scores.shape: {positive_scores.shape}")
            loss = np.mean(-np.log(positive_scores))

            one_hot = np.zeros_like(scores)
            one_hot[np.arange(labels.shape[0]), labels] = 1
            grad = (scores - one_hot) / scores.shape[0]
            return loss, grad
        self.loss = softmax_cross_entropy

        # layers part
        # TODO: 两层很多东西都很像，可以作为两个子类抽象出一部分功能实现
        # linear layer
        class LinearLayer():
            def __init__(self, input_size, output_size):
                self.input_size = input_size
                self.output_size = output_size
                self.weights = np.random.normal(0, 0.3, (input_size, output_size))
                self.biases = np.zeros((1, output_size))
                self.is_train = False
                self.last_input = None  # for Back Propagation

            def forward(self, x):
                if self.is_train:
                    self.last_input = x
                # xW + b
                return np.dot(x, self.weights) + self.biases

            def backward(self, grad_y):
                if self.last_input is None:
                    err_msg = "No input data for back propagation."
                    logging.error(err_msg)
                    raise RuntimeError(err_msg)
                grad_biases = np.sum(grad_y, axis=0, keepdims=True)
                grad_weights = np.dot(self.last_input.T, grad_y)
                grad_x = np.dot(grad_y, self.weights.T)
                return grad_x, self.weights, grad_weights, self.biases, grad_biases

            def train(self):
                self.is_train = True

            def eval(self):
                self.is_train = False
        # end for LinearLayer class

        # activation layer: tanh
        class Tanh():
            def __init__(self):
                self.is_train = False
                self.last_input = None

            def forward(self, x):
                if self.is_train:
                    self.last_input = x
                return np.tanh(x)

            def backward(self, grad_y):
                # return data: grad_x, self.weights, grad_weights, self.biases, grad_biases (from linear layer)
                # tanh derivative: 1 - tanh(x) ^ 2
                return (1 - np.power(np.tanh(self.last_input), 2)) * grad_y, None, None, None, None

            def train(self):
                self.is_train = True

            def eval(self):
                self.is_train = False
        # end for activation layer

        self.layers = []
        for i, size in enumerate(layer_sizes[: -1]):
            # linear layer
            layer = LinearLayer(layer_sizes[i], layer_sizes[i + 1])
            self.layers.append(layer)
            # activation layer
            if i < len(layer_sizes) - 2:
                self.layers.append(Tanh())

    def forward(self, x):
        # 前向传播
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, inputs, labels, lr):  # 自行确定参数表
        # 反向传播
        weights_layers = []
        grad_weights_layers = []
        biases_layers = []
        grad_biases_layers = []
        preds = self.forward(inputs)
        loss, grad = self.loss(preds, labels)  # softmax_cross_entropy
        # reverse layers for back propagation
        for layer in reversed(self.layers):
            grad, weights, grad_weights, biases, grad_biases = layer.backward(grad)
            if weights is not None:  # linear layer
                # for updating weights and bias
                # update after the traverse(IMPORTANT POINT)
                weights_layers.append(weights)
                grad_weights_layers.append(grad_weights)
                biases_layers.append(biases)
                grad_biases_layers.append(grad_biases)
        for weight, grad_weight, biases, grad_bias in zip(weights_layers, grad_weights_layers, biases_layers, grad_biases_layers):
            weight -= grad_weight * lr
            biases -= grad_bias * lr
        return loss

    def train(self):
        for layer in self.layers:
            layer.train()

    def eval(self):
        for layer in self.layers:
            layer.eval()


def train(mlp: MLP, epochs, lr, inputs, labels):
    '''
        mlp: 传入实例化的MLP模型
        epochs: 训练轮数
        lr: 学习率
        inputs: 生成的随机数据
        labels: 生成的one-hot标签
    '''
    # TODO: add batch size and shuffle
    mlp.train()
    input_labels = np.argmax(labels, axis=1)
    loss_list = []
    for epoch in range(epochs):
        loss = mlp.backward(inputs, input_labels, lr)
        loss_list.append(loss)
        logging.info(f"epoch: {epoch}, loss: {loss}")
    return loss_list


def train_torch_mlp(epochs, lr, inputs, labels):
    # 为了对比一致，不使用用batch和shuffle
    class TorchMLP(torch.nn.Module):
        def __init__(self):
            super(TorchMLP, self).__init__()
            self.layers = torch.nn.Sequential(
                torch.nn.Linear(10, 10),
                torch.nn.Tanh(),
                torch.nn.Linear(10, 8),
                torch.nn.Tanh(),
                torch.nn.Linear(8, 8),
                torch.nn.Tanh(),
                torch.nn.Linear(8, 4)
            )
            self.loss = torch.nn.CrossEntropyLoss()

        def forward(self, x):
            return self.layers(x)

    net = TorchMLP()
    net.train()
    optim = torch.optim.SGD(net.parameters(), lr=lr)
    input_labels = np.argmax(labels, axis=1)
    loss_list = []
    for epoch in range(epochs):
        inputs_tensor = torch.tensor(inputs, dtype=torch.float32)
        labels_tensor = torch.tensor(input_labels, dtype=torch.long)
        pred = net(inputs_tensor)
        loss = net.loss(pred, labels_tensor)
        loss_list.append(loss.item())
        optim.zero_grad()
        loss.backward()
        optim.step()
        logging.info(f"epoch: {epoch}, loss: {loss.item()}")
    return loss_list


if __name__ == '__main__':
    # 设置随机种子,保证结果的可复现性
    np.random.seed(1)
    mlp = MLP()
    # 生成数据
    inputs = np.random.randn(100, 10)

    # 生成one-hot标签
    # 修改了助教代码，保证labels的数据类型为int
    labels = np.eye(4, dtype=np.int64)[np.random.randint(0, 4, size=(1, 100))].reshape(100, 4)
    logging.debug(f"labels.shape: {labels.shape}")
    logging.debug(f"labels.dtype: {labels.dtype}")

    # 训练
    epochs = 2000
    lr = 0.1
    loss_list = train(mlp, epochs, lr, inputs, labels)
    # print weights and bias
    for i, layer in enumerate(mlp.layers):
        if i % 2 == 0:
            print(f"Layer {i // 2} weights:")
            print(layer.weights)
            print(f"Layer {i // 2} bias:")
            print(layer.biases)
    # torch_loss_list = train_torch_mlp(epochs, lr, inputs, labels)
    # plt.ylim(-0.1, 2.0)
    # plt.plot(loss_list, label='Manual MLP')
    # plt.plot(torch_loss_list, label='Torch MLP')
    # plt.legend()
    # plt.show()
