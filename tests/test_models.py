import tensorflow as tf
import tflearn
import unittest
import os

class TestModels(unittest.TestCase):
    """
    Testing DNN model from tflearn/models/dnn.py
    """

    def test_dnn(self):

        with tf.Graph().as_default():
            X = [3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,7.042,10.791,5.313,7.997,5.654,9.27,3.1]
            Y = [1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,2.827,3.465,1.65,2.904,2.42,2.94,1.3]
            input = tflearn.input_data(shape=[None])
            linear = tflearn.single_unit(input)
            regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                            metric='R2', learning_rate=0.01)
            m = tflearn.DNN(regression)
            # Testing fit and predict
            m.fit(X, Y, n_epoch=1000, show_metric=True, snapshot_epoch=False)
            res = m.predict([3.2])[0]
            self.assertGreater(res, 1.3, "DNN test (linear regression) failed! with score: " + str(res) + " expected > 1.3")
            self.assertLess(res, 1.8, "DNN test (linear regression) failed! with score: " + str(res) + " expected < 1.8")

            # Testing save method
            m.save("test_dnn.tflearn")
            self.assertTrue(os.path.exists("test_dnn.tflearn"))

        with tf.Graph().as_default():
            input = tflearn.input_data(shape=[None])
            linear = tflearn.single_unit(input)
            regression = tflearn.regression(linear, optimizer='sgd', loss='mean_square',
                                            metric='R2', learning_rate=0.01)
            m = tflearn.DNN(regression)

            # Testing load method
            m.load("test_dnn.tflearn")
            res = m.predict([3.2])[0]
            self.assertGreater(res, 1.3, "DNN test (linear regression) failed after loading model! score: " + str(res) + " expected > 1.3")
            self.assertLess(res, 1.8, "DNN test (linear regression) failed after loading model! score: " + str(res) + " expected < 1.8")

    def test_sequencegenerator(self):

        with tf.Graph().as_default():
            text = "123456789101234567891012345678910123456789101234567891012345678910"
            maxlen = 5

            X, Y, char_idx = \
                tflearn.data_utils.string_to_semi_redundant_sequences(text, seq_maxlen=maxlen, redun_step=3)

            g = tflearn.input_data(shape=[None, maxlen, len(char_idx)])
            g = tflearn.lstm(g, 32)
            g = tflearn.dropout(g, 0.5)
            g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
            g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                                   learning_rate=0.1)

            m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                                          seq_maxlen=maxlen,
                                          clip_gradients=5.0)
            m.fit(X, Y, validation_set=0.1, n_epoch=100, snapshot_epoch=False)
            res = m.generate(10, temperature=.5, seq_seed="12345")
            self.assertEqual(res, "123456789101234", "SequenceGenerator test failed! Generated sequence: " + res + " expected '123456789101234'")

            # Testing save method
            m.save("test_seqgen.tflearn")
            self.assertTrue(os.path.exists("test_seqgen.tflearn"))

            # Testing load method
            m.load("test_seqgen.tflearn")
            res = m.generate(10, temperature=.5, seq_seed="12345")
            # TODO: Fix test
            #self.assertEqual(res, "123456789101234", "SequenceGenerator test failed after loading model! Generated sequence: " + res + " expected '123456789101234'")

if __name__ == "__main__":
    unittest.main()
