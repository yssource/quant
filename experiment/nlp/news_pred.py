import gensim
import numpy as np
import tensorflow as tf

model = gensim.models.Word2Vec.load("/home/canl/quant/data/stocknet-dataset/news_word2vec.model")
data_map = np.load('/home/canl/quant/data/stocknet-dataset/data_map.npy').tolist()
w2v_embd_size = np.load('/home/canl/quant/data/stocknet-dataset/w2v_embd_size.npy')

def avg_embedding(news_word_list, array_size = w2v_embd_size):
  sum_array = np.array([0.0]*w2v_embd_size)
  for word in news_word_list:
    sum_array += model[word]
  return sum_array/len(news_word_list)

max_news_num = 10

class mlp(object):
  def __init__(self, lstm_size=100, num_class = 3, max_news_num = max_news_num, train_day = 5, w2v_size =w2v_embd_size):
    self.lstm_size = lstm_size
    self.learning_rate = 0.1
    self.w2v_size = w2v_size
    self.num_class = num_class
    self.train_day = train_day
    self.max_news_num = max_news_num
    self.create_placeholder()
    self.create_bilstm()
    self.create_discriminator()
    self.run_init()

  def create_placeholder(self, mode):
    self.news_input = tf.placeholder(tf.float32, [None, self.train_day, self.max_news_num, self.w2v_size])  # batch size = max_news_num in one day
    self.y = tf.placeholod(tf.int32, [None, self.num_class])

  def create_inday_attention(self):
    self.inday_attention = tf.Variable(tf.random_normal([self.train_day, self.max_news_num]))
    self.day_news = tf.reduce_sum(tf.multiply(self.news_input, self.inday_attention), 2)  # should be (batch_size, train_day, w2v_size)

  def create_bigru(self):
    #self.fw = tf.contrib.rnn.BasicLSTMCell(embd_size, forget_bias=1.0)
    self.fw = tf.nn.rnn_cell.GRUCell(self.lstm_size, input_size=None, activation=tanh)
    self.bw = tf.nn.rnn_cell.GRUCell(self.lstm_size, input_size=None, activation=tanh)
    self.bilstm_embd = tf.contrib.rnn.static_bidirectional_rnn(fw, bw, self.day_news, dtype=tf.float32) # should be (batch_size, train_day, 2*lstm_size)

  def create_news_seq_attention(self):
    self.news_seq_attention = tf.Variable(tf.random_normal([self.train_day]))
    self.output_v = tf.reduce_sum(tf.multiply(self.bilstm_embd, self.news_seq_attention), 1)  # should be (batch_size, 2*lstm_size)

  def create_discriminator(self):
    self.dis_weights = tf.Variable(tf.random_normal([2*self.lstm_size, self.num_class]))
    self.pred_v = tf.nn.softmax(tf.matmul(self.output_v, self.dis_weights))  # should be (batch_size, num_class)
    self.pred = tf.argmax(self.pred_v, 1)  # should be [batch_size]

  def create_loss(self):
    self.loss = tf.nn.softmax_cross_entropy_with_logits(logits=self.pred_v, labels=tf.one_hot(self.y, self.num_class))
    self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)

  def predict(self, news, labels):
    return self.sess.run(self.pred, feed_dict = {self.news_input:news, self.y:labels})

  def fit(self, news, labels):
    loss, opt = self.sess.run((self.loss, self.optimizer), feed_dict = {self.news_input:news, self.y:labels})
    return loss, opt

  def run_init(self):
    init = tf.global_variables_initializer()
    self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
    self.sess.run(init)

aapl = data_map['AAPL']

def generate_one_train(pd):
  length = len(pd)
  index = random.randint(0, length-2)
  record = pd[index:index+1]
  label = record['label']
  news = record['news'][0].values()
  news_list = []
  for day_news in news:
    for block_news in day_news:
      for word in block_news:
        news_list.append(model[word])
  return news_list, label, index

m = mlp()
news_list, label, index = generate_one_train(aapl)
m.fit(news_list, labels=label)
