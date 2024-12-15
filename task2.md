# Task 2  

Bu model Müşteri veya temsilcisinden konuşma geldikçe sentiment/intent buluyor.  
Sizce bu sistemi (BART modelini değiştirmeden) conversational AI modeli gibi çalışacak hale getirmek için ne gibi hızlı ‘quick’ çözümler kullanabiliriz?

## Cevap  

Kullandığım model `facebook/bart-large-mnli` isimli BART modeli olduğundan ve bu model generating üzerine olmayıp verilen  
labellara göre classification yapmak üzerine eğitilmiş bir model olduğu için burada doğrudan (modelde hiçbir değişiklik yapmadan)  
`.generate` fonksiyonunu çağırarak conversational AI modeli gibi çalıştıramayız. Ancak yine de modelin classification yeteneğinden  
faydalanarak bu amacımıza ulaşmamız mümkün.  

### Adımlar  

#### 1. Labelların Özelleştirilmesi  

Öncelikle labellarımızı daha özelleştirmeliyiz. Örneğin, modelde ben genel intention'ın anlaşılması için şu labelları kullanmıştım:  

`["buy", "upgrade", "information", "greeting", "confirm", "decline", "choose"]`  

Ancak bu labellar düzgün bir conversational yaratmak için yeterli değil. Bu labellara örneğin:  

- `"ask about payment due date"`  
- `"request refund"`  
- `"technical support for internet"`  
- `"technical support for phone"`  

gibi daha özelleştirilmiş labelları eklemeliyiz.  

#### 2. Templatelerin Hazırlanması  

Arttırılmış intention labellarımızla sentiment labellarımızın her birinin kombinasyonu için hazır templateler oluşturmalıyız.  

```python
response_templates = {
    # Ask about payment due date
    ("ask about payment due date", "negative"): "I understand there might be concerns about your payment due date. Let me assist you immediately.",
    ("ask about payment due date", "neutral"): "Your payment due date is important to us. Let me check that for you.",
    ("ask about payment due date", "positive"): "Thank you for checking your payment due date proactively! Let me provide you with the details.",

    # Request refund
    ("request refund", "negative"): "I'm sorry you need a refund. Let me assist you with the process.",
    ("request refund", "neutral"): "You're requesting a refund. Let me guide you through the steps to process it.",
    ("request refund", "positive"): "Thank you for letting us know about your refund request! Let’s resolve it promptly for you.",

    # Technical support for internet
    ("technical support for internet", "negative"): "I understand you're having trouble with your internet. Let's fix it as quickly as possible.",
    ("technical support for internet", "neutral"): "You're facing an issue with your internet connection. Let me check what’s going on.",
    ("technical support for internet", "positive"): "Thank you for reaching out about your internet. Let's ensure everything is running smoothly!",

    # Technical support for phone
    ("technical support for phone", "negative"): "I see there's an issue with your phone service. Let me help you resolve it right away.",
    ("technical support for phone", "neutral"): "You're reporting a phone service issue. I'll take care of it for you.",
    ("technical support for phone", "positive"): "Thank you for letting us know about your phone service. I'll ensure it’s resolved efficiently!"
}
```

#### 3. Templatelerin Dinamikleştirilmesi

Hatta istersek bu templateleri daha doğal bir konuşma akışı için şu şekilde dinamikleştirebiliriz:

```python
("technical support for internet", "negative"): "I see you're asking about {user_input}. Could you provide more details?"
```

### Uygulama

Templatelerimizi ayarladıktan sonra modelimize user inputu için sentiment ve intention labellarıyla classification yaptırıp,
çıkan sonuca göre ekrana eşleşen templateleri bastırırız ve böylece BART modelimizi değiştirmeden conversational AI modeli gibi çalışacak hale getirmiş oluruz.