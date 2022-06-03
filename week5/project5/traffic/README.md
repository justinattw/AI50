I initially tried using the same model as the 
Handwriting demo, as I thought the image size of 
30*30 was close enough to 28*28 to produce decent
results. This faltered, resulting in a model
that gave a very poor 6% accuracy.

I based my work on this handwriting model, firstly
increasing the number of filters tried in the
first convolutional layer from 32 to 64 (while
still using a 3*3 kernel). I also maintained the
max-pooling layer wiht a 2x2 pool size.

I increased the number of hidden layers from 1 
layer to 3 layers of 128 units each.Because I 
had more hidden layers, I  lowered the dropout 
rate at each layer to 0.15.

This model gave an accuracy of 58-60%; better, but 
still not great.

I decided to add another convolutional layer
after the max-pooling layer, again learning 64
different filters. This is my final model, which
gives an accuracy of around 95-96%.

