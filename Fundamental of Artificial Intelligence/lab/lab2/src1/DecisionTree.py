import numpy as np
import logging


# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# )


class DecisionTree():
    def __init__(self, max_depth=32, min_sample_split=2):
        self.root = None
        self.max_depth = max_depth
        self.min_sample_split = min_sample_split

    def fit(self, train_features, train_labels):
        '''
        TODO: 实现决策树学习算法.
        train_features是维度为(训练样本数,属性数)的numpy数组
        train_labels是维度为(训练样本数, )的numpy数组
        '''
        self.root = self._tree_generate(train_features, train_labels, 0)
        # logging.debug(f"type(self.root.value): {type(self.root.value)}")

    def predict(self, test_features):
        '''
        TODO: 实现决策树预测.
        test_features是维度为(测试样本数,属性数)的numpy数组
        该函数需要返回预测标签，返回一个维度为(测试样本数, )的numpy数组
        '''
        predictions = [self._predict(features) for features in test_features]
        logging.debug(f"predictions: {predictions}")
        return np.asarray(predictions)

    # define decision node class
    class DecisionNode():
        def __init__(
            self, feature_idx, threshold, true_branch, false_branch, value
        ):
            self.feature_idx = feature_idx
            self.threshold = threshold
            self.true_branch = true_branch
            self.false_branch = false_branch
            # logging.debug(f"type(feature_idx): {type(feature_idx)}")
            # logging.debug(f"type(value): {type(value)}")
            self.value = value

    # generate decision tree
    def _tree_generate(self, features, labels, depth):
        info_gain_max = 0
        num_samples, num_features = features.shape
        # logging.debug(
        #     f"num_samples: {num_samples}, num_features: {num_features}"
        # )
        # labels.shape (num_samples, 1)
        labels = np.expand_dims(labels, axis=1)
        # join feature and label to a table with num_samples rows
        # features_labels.shape (num_samples, num_features+1)
        features_labels = np.concatenate((features, labels), axis=1)
        # logging.debug(f"features_labels.shape: {features_labels.shape}")

        if num_samples >= self.min_sample_split and depth <= self.max_depth:
            # for each feature
            for feature_idx in range(num_features):
                # feature_vals.shape (num_samples, 1)
                feature_vals = np.expand_dims(features[:, feature_idx], axis=1)
                # unique_vals is the all values of this feature
                unique_vals = np.unique(feature_vals)
                for value in unique_vals:
                    logging.debug(f"feature_idx: {feature_idx}")
                    logging.debug(f"value: {value}")
                    logging.debug(f"features_labels[:, feature_idx]: {features_labels[:, feature_idx]}")
                    fl_less_than_value = features_labels[
                        features_labels[:, feature_idx] < value
                    ]
                    fl_not_less_than_value = features_labels[
                        features_labels[:, feature_idx] >= value
                    ]
                    logging.debug(f"{fl_less_than_value.size > 0 and fl_not_less_than_value.size > 0}")
                    if fl_less_than_value.size > 0 and fl_not_less_than_value.size > 0:
                        # label_less_than_value = fl_less_than_value[:, num_features:]
                        # label_not_less_than_value = fl_not_less_than_value[:, num_features:]
                        label_less_than_value = np.expand_dims(fl_less_than_value[:, -1], axis=1)
                        label_not_less_than_value = np.expand_dims(fl_not_less_than_value[:, -1], axis=1)
                        info_gain = DecisionTree.calc_info_gain(labels, label_less_than_value, label_not_less_than_value)
                        logging.debug(f"info_gain: {info_gain}")
                        if info_gain > info_gain_max:
                            info_gain_max = info_gain
                            best_feature_idx = feature_idx
                            best_threshold = value
                            best_division = (fl_less_than_value, fl_not_less_than_value)
        if info_gain_max > 0:
            logging.debug("Innder node.")
            true_branch = self._tree_generate(best_division[0][:, :-1], best_division[0][:, -1], depth + 1)
            false_branch = self._tree_generate(best_division[1][:, :-1], best_division[1][:, -1], depth + 1)
            return DecisionTree.DecisionNode(
                feature_idx=best_feature_idx,
                threshold=best_threshold,
                true_branch=true_branch,
                false_branch=false_branch,
                value=None,
            )
        else:
            logging.debug("Leaf node.")
            max_count = 0
            label_pred = None
            for label in np.unique(labels):
                count = labels[labels == label].shape[0]
                if count > max_count:
                    max_count = count
                    label_pred = label
            return DecisionTree.DecisionNode(
                feature_idx=None,
                threshold=None,
                true_branch=None,
                false_branch=None,
                value=label_pred,
            )

    # calculate entropy
    @staticmethod
    def calc_entropy(labels):
    # def calc_entropy(labels, all_labels):
        # assertion about the shape of labels
        assert(len(labels.shape) == 2 and labels.shape[1] == 1)
        unique_labels = np.unique(labels)
        entropy = 0
        num_all_labels = labels.shape[0]
        # num_all_labels = all_labels.shape[0]
        label_count = 0  # for debug
        for label in unique_labels:
            # logging.debug(f"labels.shape: {labels.shape}")
            # logging.debug(f"labels: {labels}")
            # logging.debug(f"label: {label}")
            tmp = (labels[labels == label].shape[0]) / num_all_labels
            logging.debug(f"tmp = {labels[labels == label].shape[0]} / {num_all_labels} = {tmp}")
            # tmp = (all_labels[all_labels == label].shape[0]) / num_all_labels
            entropy += - (tmp * np.log2(tmp))
            label_count += labels[labels == label].shape[0]  # for debug
            logging.debug(f"num of this target label: {labels[labels == label].shape[0]}")
        assert(label_count == labels.shape[0])
        return entropy

    # calculate info gain
    @staticmethod
    def calc_info_gain(labels, labels1, labels2):
        # assertion about labels
        assert(len(labels.shape) == 2 and labels.shape[1] == 1)
        assert(len(labels1.shape) == 2 and labels1.shape[1] == 1)
        assert(len(labels2.shape) == 2 and labels2.shape[1] == 1)
        assert(labels.shape[0] == labels1.shape[0] + labels2.shape[0])

        tmp = labels1.shape[0] / labels.shape[0]
        info_gain = DecisionTree.calc_entropy(labels) - tmp * DecisionTree.calc_entropy(labels1) - (1 - tmp) * DecisionTree.calc_entropy(labels2)
        # info_gain = DecisionTree.calc_entropy(labels, labels) - tmp * DecisionTree.calc_entropy(labels1, labels) - (1 - tmp) * DecisionTree.calc_entropy(labels2, labels)
        return info_gain

    def _predict(self, features):
        # default begin from tree root
        if not self.root:
            logging.warning("self.root is None.")
        node = self.root
        while node.value is None:
            feature_value = features[node.feature_idx]
            if feature_value < node.threshold:
                node = node.true_branch
            else:
                node = node.false_branch
        return node.value


# treenode: [attr, feat[attr] == 1, feat[attr] == 2, feat[attr] == 3]


if __name__ == "__main__":
    labels = np.asarray([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1]).reshape(12, 1)
    entropy = DecisionTree.calc_entropy(labels=labels)
    # entropy = DecisionTree.calc_entropy(labels=labels, all_labels=labels)
    print(entropy)
