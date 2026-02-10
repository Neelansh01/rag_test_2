# Sample Questions & Expected Responses  
## For PDF: *Think and Grow Rich* (Author's Preface, 6 pages)

Use these in your RAG app after uploading the PDF and clicking **Store in ChromaDB**.

---

### 1. **Who gave the author the money-making secret?**  
**Prompt:** Who gave the author the money-making secret?  
**Expected response (from the document):** Andrew Carnegie. He shared it with the author more than a quarter of a century ago when the author was young; Carnegie then asked if he would spend twenty years or more preparing to take it to the world.

---

### 2. **What was Charles M. Schwab’s role and what was it worth?**  
**Prompt:** What did Charles M. Schwab do with the formula and how much was it worth?  
**Expected response:** Charles M. Schwab conceived and carried out the organization of the giant United States Steel Corporation. That single application of the secret made him a huge fortune in money and opportunity—roughly **six hundred million dollars**.

---

### 3. **Can the secret be bought or given away?**  
**Prompt:** Can the secret be purchased or given away?  
**Expected response:** No. The secret cannot be given away and cannot be purchased for money because it comes in **two parts**, and one part is already in the possession of those who are ready for it. It cannot be had at any price by those who are not intentionally searching for it.

---

### 4. **Which famous people used the secret?**  
**Prompt:** Name some famous people who used the Carnegie secret.  
**Expected response:** The book lists many, including: Henry Ford, John D. Rockefeller, Thomas A. Edison, Charles M. Schwab, Woodrow Wilson, William Wrigley Jr., John Wanamaker, Arthur Nash, Jennings Randolph, Stuart Austin Wier, Frank A. Vanderlip, F. W. Woolworth, and others. Edison had only three months of schooling.

---

### 5. **What did Arthur Nash do with the formula?**  
**Prompt:** What did Arthur Nash do with the formula?  
**Expected response:** Arthur Nash was a Cincinnati tailor who used his near-bankrupt business as a “guinea pig” to test the formula. The business came to life and made a fortune for its owners; the experiment received more than a million dollars’ worth of laudatory publicity in newspapers and magazines.

---

### 6. **What does the book say about education and schooling?**  
**Prompt:** What does the book say about education and schooling?  
**Expected response:** Many of the people who used the secret had very little schooling. Henry Ford never reached high school. John Wanamaker said he acquired what little schooling he had “in very much the same manner as a modern locomotive takes on water, by scooping it up as it runs.” The book states that those who master and apply the secret can reach high stations and accumulate riches even with meager schooling. “What is EDUCATION” is answered in full detail in the book.

---

### 7. **How is the secret presented in the book?**  
**Prompt:** How is the secret revealed in the book—is it named directly?  
**Expected response:** The secret is not directly named. It has been mentioned no fewer than a hundred times and is “merely uncovered and left in sight” so that those who are ready and searching for it may pick it up. Carnegie tossed it to the author quietly without giving its specific name. If you are ready, you will recognize it at least once in every chapter.

---

### 8. **What did President Woodrow Wilson do with the secret?**  
**Prompt:** How did Woodrow Wilson use the secret?  
**Expected response:** President Woodrow Wilson used the secret extensively during the World War. It was passed on to every soldier who fought in the war, wrapped in the training they received before going to the front. Wilson told the author it was a strong factor in raising the funds needed for the war.

---

### 9. **What should the reader do when they recognize the secret?**  
**Prompt:** What should you do when the secret appears to you while reading?  
**Expected response:** When the secret “jump[s] from the page and stand[s] boldly before you,” you should stop for a moment and **turn down a glass**—that occasion will mark the most important turning point of your life.

---

### 10. **What is the book’s purpose?**  
**Prompt:** What is the purpose of Think and Grow Rich?  
**Expected response:** The book deals with facts, not fiction. Its purpose is to convey a great universal truth through which all who are READY may learn **what to do**, **how to do it**, and receive **the needed stimulus to make a start**. It addresses problems of earning a living, finding hope, courage, contentment and peace of mind, accumulating riches, and enjoying freedom of body and spirit.

---

## How to use in your RAG app

1. Upload **Think-And-Grow-Rich_2011-06-pages.pdf** in the app.
2. Run the pipeline (collection → cleaning → chunking → embedding).
3. Click **Store in ChromaDB**.
4. Type any of the prompts above in the **Your question** box.
5. Check that the **retrieved chunks** contain the relevant sentences, and that the **Answer / Context sent to LLM** section includes that content.

*(In a full RAG setup with an LLM, the model would generate a short answer from that context; in this demo you see the context that would be sent.)*
