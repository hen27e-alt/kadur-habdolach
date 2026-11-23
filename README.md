# כדור בדולח

אפליקציית בידור מיסטית בעברית: כדור בדולח אינטראקטיבי, קלף היום ופריסת שלושה קלפים, מזלות, נומרולוגיה (גימטריה) ויומן אישי.
דף אחד (`index.html`), בלי build ובלי תלויות. הנתונים נשמרים בדפדפן בלבד (`localStorage`, מפתחות `kadur_*`).
המענים נוצרים מקומית ומיועדים לבידור בלבד.

## הרצה מקומית
```
python3 -m http.server 8000
```
ואז לפתוח http://localhost:8000

## פריסה

### Firebase Hosting
1. ליצור פרויקט ב-Firebase בשם `kadur-habdolach` (או כל שם אחר ולעדכן את `.firebaserc` ואת `projectId` ב-workflow).
2. `firebase deploy --only hosting`
3. פריסה אוטומטית ב-push ל-`main`: להריץ פעם אחת `firebase init hosting:github` (יוצר את הסוד `FIREBASE_SERVICE_ACCOUNT`). בלי הסוד ה-workflow מדלג ולא נכשל.

### Vercel
לייבא את הריפו ב-vercel.com/new. זה אתר סטטי, אז אין צורך ב-Framework, Build Command או Output Directory (`vercel.json` כבר קיים).

## הטמעה
האפליקציה נפתחת גם בתוך ה-CRM (כפתור "← CRM" מופיע רק בתוך iframe). הגרסה המתארחת ב-CRM נמצאת ב-`hen27e-alt/crm-fix` בנתיב `/kadur/`.
