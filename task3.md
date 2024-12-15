# Task 3 (İsteğe Bağlı) 

Bu Modeli Nasıl Hızlandırırız?

## Cevap

BART modellerinin hızı **input-output boyutları** ile ilgilidir. Bu caseimizde de etiketlerimiz çok uzun olmadığı için outputtan ziyade daha çok input üzerinde data preprocessing yaparak modelimizin hızını arttırabiliriz. Örneğin inputları stemming ya da lemmatization gibi tekniklerle köklerine kadar indirgeyerek inputumuzu kısaltabiliriz. Bu da inputların vektörler haline getirilme süresini kısaltacaktır. Modelimiz de conversational bir model olmadığı, similarity ile tahmin üzerinden çalıştığı için bu yöntemler performansı düşürmeyecek, hatta belli koşullarda performansı yükseltecektir.

Bunun dışında vektörlerde tutulan sayı türünü küçülterek (örneğin float32 den float16 ya) hızımızı arttırabiliriz. Ancak bu verilerimizin precision değerini azaltarak modelin başarısını bir miktar düşürebilir.

Son olarak vektörler ile PCA algoritması kullanarak boyut küçültme yoluna gidebilir ve bu şekilde modelimizi hızlandırabiliriz. Ancak bu da diversityi azaltacağı için PCA hiperparametresi düzgün seçilmelidir.

**NOT**: Eğer modeli modifiye etme şansımız varsa belli layerlar atılarak veya küçültülerek yeniden fine-tune edilip daha küçük bir modele dönüştürülebilir ve bu da tabii ki hızı arttıracaktır.
