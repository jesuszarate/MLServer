import tensorflow as tf

# from tensorflow.example.tutorials.mnist input_data
# mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

#from tensorflow.examples.tutorials.mnist import input_data
#mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# 10 classes, 0-9

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 10
batch_size = 100

x = tf.placeholder('float'[None, 784])
y = tf.placeholder('float')


def newral_network_model(data):
    hidden_1_layer = {'weight': tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal(n_nodes_hl1))}

    hidden_2_layer = {'weight': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal(n_nodes_hl2))}

    hidden_3_layer = {'weight': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal(n_nodes_hl3))}                                    

    output_layer = {'weight': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                      'biases': tf.Variable(tf.random_normal(n_classes))}

    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']) + hidden_1_layer['biases'])                    
    l1 = tf.nn.relu(l1) # Threshold function

    l2 = tf.add(tf.matmul(hidden_1_layer, hidden_2_layer['weights']) + hidden_2_layer['biases'])                    
    l2 = tf.nn.relu(l2) # Threshold function

    l3 = tf.add(tf.matmul(hidden_2_layer, hidden_3_layer['weights']) + hidden_3_layer['biases'])                    
    l3 = tf.nn.relu(l3) # Threshold function

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']
    
    return output
