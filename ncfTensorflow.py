#-------------
# HYPERPARAMS
#-------------

num_neg = 6
latent_features = 8
epochs = 20
batch_size = 256
learning_rate = 0.001


#-------------------------
# TENSORFLOW GRAPH
#-------------------------

graph = tf.Graph()

with graph.as_default():

    # Define input placeholders for user, item and label.
    user = tf.placeholder(tf.int32, shape=(None, 1))
    item = tf.placeholder(tf.int32, shape=(None, 1))
    label = tf.placeholder(tf.int32, shape=(None, 1))

    # User embedding for MLP
    mlp_u_var = tf.Variable(tf.random_normal([len(users), 32], stddev=0.05),
            name='mlp_user_embedding')
    mlp_user_embedding = tf.nn.embedding_lookup(mlp_u_var, user)

    # Item embedding for MLP
    mlp_i_var = tf.Variable(tf.random_normal([len(items), 32], stddev=0.05),
            name='mlp_item_embedding')
    mlp_item_embedding = tf.nn.embedding_lookup(mlp_i_var, item)

    # User embedding for GMF
    gmf_u_var = tf.Variable(tf.random_normal([len(users), latent_features],
        stddev=0.05), name='gmf_user_embedding')
    gmf_user_embedding = tf.nn.embedding_lookup(gmf_u_var, user)

    # Item embedding for GMF
    gmf_i_var = tf.Variable(tf.random_normal([len(items), latent_features],
        stddev=0.05), name='gmf_item_embedding')
    gmf_item_embedding = tf.nn.embedding_lookup(gmf_i_var, item)

    # Our GMF layers
    gmf_user_embed = tf.keras.layers.Flatten()(gmf_user_embedding)
    gmf_item_embed = tf.keras.layers.Flatten()(gmf_item_embedding)
    gmf_matrix = tf.multiply(gmf_user_embed, gmf_item_embed)

    # Our MLP layers
    mlp_user_embed = tf.keras.layers.Flatten()(mlp_user_embedding)
    mlp_item_embed = tf.keras.layers.Flatten()(mlp_item_embedding)
    mlp_concat = tf.keras.layers.concatenate([mlp_user_embed, mlp_item_embed])

    mlp_dropout = tf.keras.layers.Dropout(0.2)(mlp_concat)

    mlp_layer_1 = tf.keras.layers.Dense(64, activation='relu', name='layer1')(mlp_dropout)
    mlp_batch_norm1 = tf.keras.layers.BatchNormalization(name='batch_norm1')(mlp_layer_1)
    mlp_dropout1 = tf.keras.layers.Dropout(0.2, name='dropout1')(mlp_batch_norm1)

    mlp_layer_2 = tf.keras.layers.Dense(32, activation='relu', name='layer2')(mlp_dropout1)
    mlp_batch_norm2 = tf.keras.layers.BatchNormalization(name='batch_norm1')(mlp_layer_2)
    mlp_dropout2 = tf.keras.layers.Dropout(0.2, name='dropout1')(mlp_batch_norm2)

    mlp_layer_3 = tf.keras.layers.Dense(16, activation='relu', name='layer3')(mlp_dropout2)
    mlp_layer_4 = tf.keras.layers.Dense(8, activation='relu', name='layer4')(mlp_layer_3)

    # We merge the two networks together
    merged_vector = tf.keras.layers.concatenate([gmf_matrix, mlp_layer_4])

    # Our final single neuron output layer.
    output_layer = tf.keras.layers.Dense(1,
            kernel_initializer="lecun_uniform",
            name='output_layer')(merged_vector)

    # Our loss function as a binary cross entropy.
    loss = tf.losses.sigmoid_cross_entropy(label, output_layer)

    # Train using the Adam optimizer to minimize our loss.
    opt = tf.train.AdamOptimizer(learning_rate = learning_rate)
    step = opt.minimize(loss)

    # Initialize all tensorflow variables.
    init = tf.global_variables_initializer()


session = tf.Session(config=None, graph=graph)
session.run(init)
