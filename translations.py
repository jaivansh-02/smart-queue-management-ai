# translations.py — All UI text + email/notification translations
# Supported: English, Hindi, French, Spanish, German, Arabic, Bengali, Marathi

LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी',
    'fr': 'Français',
    'es': 'Español',
    'de': 'Deutsch',
    'ar': 'العربية',
    'bn': 'বাংলা',
    'mr': 'मराठी',
}

# RTL languages (right to left)
RTL_LANGUAGES = ['ar']

TRANSLATIONS = {

    # ── NAVIGATION ────────────────────────────────────────────────────────────
    'nav_home':        {'en':'Home','hi':'होम','fr':'Accueil','es':'Inicio','de':'Startseite','ar':'الرئيسية','bn':'হোম','mr':'मुखपृष्ठ'},
    'nav_display':     {'en':'Display','hi':'डिस्प्ले','fr':'Affichage','es':'Pantalla','de':'Anzeige','ar':'العرض','bn':'ডিসপ্লে','mr':'प्रदर्शन'},
    'nav_patient':     {'en':'Patient','hi':'मरीज़','fr':'Patient','es':'Paciente','de':'Patient','ar':'المريض','bn':'রোগী','mr':'रुग्ण'},
    'nav_doctor':      {'en':'Doctor','hi':'डॉक्टर','fr':'Médecin','es':'Médico','de':'Arzt','ar':'الطبيب','bn':'ডাক্তার','mr':'डॉक्टर'},
    'nav_admin':       {'en':'Admin','hi':'एडमिन','fr':'Admin','es':'Admin','de':'Admin','ar':'المشرف','bn':'অ্যাডমিন','mr':'प्रशासक'},
    'nav_logout':      {'en':'Logout','hi':'लॉगआउट','fr':'Déconnexion','es':'Cerrar sesión','de':'Abmelden','ar':'تسجيل خروج','bn':'লগআউট','mr':'बाहेर पडा'},
    'nav_login':       {'en':'Login','hi':'लॉगिन','fr':'Connexion','es':'Iniciar sesión','de':'Anmelden','ar':'تسجيل دخول','bn':'লগইন','mr':'लॉगिन'},
    'nav_register':    {'en':'Register','hi':'रजिस्टर','fr':'S\'inscrire','es':'Registrarse','de':'Registrieren','ar':'تسجيل','bn':'নিবন্ধন','mr':'नोंदणी'},
    'nav_profile':     {'en':'Profile','hi':'प्रोफ़ाइल','fr':'Profil','es':'Perfil','de':'Profil','ar':'الملف الشخصي','bn':'প্রোফাইল','mr':'प्रोफाइल'},

    # ── HOME PAGE ─────────────────────────────────────────────────────────────
    'home_badge':      {'en':'Powered by SmartQueue AI','hi':'SmartQueue AI द्वारा संचालित','fr':'Propulsé par SmartQueue AI','es':'Impulsado por SmartQueue AI','de':'Angetrieben von SmartQueue AI','ar':'مدعوم من SmartQueue AI','bn':'SmartQueue AI দ্বারা চালিত','mr':'SmartQueue AI द्वारे चालित'},
    'home_title1':     {'en':'Smart Hospital','hi':'स्मार्ट हॉस्पिटल','fr':'Hôpital Intelligent','es':'Hospital Inteligente','de':'Intelligentes Krankenhaus','ar':'مستشفى ذكي','bn':'স্মার্ট হাসপাতাল','mr':'स्मार्ट रुग्णालय'},
    'home_title2':     {'en':'Queue + AI','hi':'कतार + AI','fr':'File + IA','es':'Cola + IA','de':'Warteschlange + KI','ar':'طابور + ذكاء اصطناعي','bn':'কিউ + এআই','mr':'रांग + एआय'},
    'home_subtitle':   {'en':'Digital tokens, AI symptom checker, health chatbot & live display — all in one.','hi':'डिजिटल टोकन, AI लक्षण जाँच, स्वास्थ्य चैटबॉट और लाइव डिस्प्ले — सब एक जगह।','fr':'Jetons numériques, vérificateur de symptômes IA, chatbot santé et affichage en direct.','es':'Tokens digitales, verificador de síntomas IA, chatbot de salud y pantalla en vivo.','de':'Digitale Token, KI-Symptomprüfer, Gesundheitschatbot und Live-Anzeige — alles in einem.','ar':'رموز رقمية وفاحص أعراض بالذكاء الاصطناعي وروبوت صحي وعرض مباشر.','bn':'ডিজিটাল টোকেন, এআই লক্ষণ পরীক্ষক, স্বাস্থ্য চ্যাটবট এবং লাইভ ডিসপ্লে।','mr':'डिजिटल टोकन, एआय लक्षण तपासक, आरोग्य चॅटबॉट आणि लाइव्ह डिस्प्ले.'},

    # ── PATIENT PORTAL ────────────────────────────────────────────────────────
    'patient_portal':  {'en':'Patient Portal','hi':'मरीज़ पोर्टल','fr':'Portail Patient','es':'Portal del Paciente','de':'Patientenportal','ar':'بوابة المريض','bn':'রোগী পোর্টাল','mr':'रुग्ण पोर्टल'},
    'patient_register':{'en':'Patient Registration','hi':'मरीज़ पंजीकरण','fr':'Inscription Patient','es':'Registro de Paciente','de':'Patientenregistrierung','ar':'تسجيل المريض','bn':'রোগী নিবন্ধন','mr':'रुग्ण नोंदणी'},
    'patient_login':   {'en':'Patient Login','hi':'मरीज़ लॉगिन','fr':'Connexion Patient','es':'Inicio de sesión del Paciente','de':'Patienten-Login','ar':'تسجيل دخول المريض','bn':'রোগী লগইন','mr':'रुग्ण लॉगिन'},
    'patient_dashboard':{'en':'Patient Dashboard','hi':'मरीज़ डैशबोर्ड','fr':'Tableau de bord Patient','es':'Panel del Paciente','de':'Patienten-Dashboard','ar':'لوحة تحكم المريض','bn':'রোগী ড্যাশবোর্ড','mr':'रुग्ण डॅशबोर्ड'},
    'welcome_back':    {'en':'Welcome back','hi':'वापस स्वागत है','fr':'Bon retour','es':'Bienvenido de nuevo','de':'Willkommen zurück','ar':'مرحباً بعودتك','bn':'স্বাগতম','mr':'पुन्हा स्वागत'},

    # ── TOKEN ─────────────────────────────────────────────────────────────────
    'your_token':      {'en':'Your Token','hi':'आपका टोकन','fr':'Votre Numéro','es':'Su Número','de':'Ihre Nummer','ar':'رقمك','bn':'আপনার টোকেন','mr':'तुमचा टोकन'},
    'get_token':       {'en':'Get Queue Token','hi':'कतार टोकन लें','fr':'Obtenir un Numéro','es':'Obtener Número','de':'Warteschlangen-Token','ar':'احصل على رقم الانتظار','bn':'কিউ টোকেন নিন','mr':'रांग टोकन मिळवा'},
    'token_generated': {'en':'Token generated!','hi':'टोकन बना!','fr':'Numéro généré!','es':'¡Número generado!','de':'Token erstellt!','ar':'تم إنشاء الرقم!','bn':'টোকেন তৈরি হয়েছে!','mr':'टोकन तयार झाला!'},
    'position':        {'en':'Position','hi':'स्थान','fr':'Position','es':'Posición','de':'Position','ar':'الموقع','bn':'অবস্থান','mr':'स्थान'},
    'est_wait':        {'en':'Est. Wait','hi':'अनुमानित प्रतीक्षा','fr':'Attente Est.','es':'Espera Est.','de':'Geschätzte Wartezeit','ar':'وقت الانتظار','bn':'আনুমানিক অপেক্ষা','mr':'अंदाजे प्रतीक्षा'},
    'waiting':         {'en':'Waiting','hi':'प्रतीक्षा','fr':'En attente','es':'Esperando','de':'Wartet','ar':'في الانتظار','bn':'অপেক্ষা','mr':'प्रतीक्षा'},
    'called':          {'en':'You are being called! Go now.','hi':'आपको बुलाया जा रहा है! अभी जाएं।','fr':'Vous êtes appelé! Allez-y maintenant.','es':'¡Te están llamando! Ve ahora.','de':'Sie werden aufgerufen! Gehen Sie jetzt.','ar':'يتم استدعاؤك! اذهب الآن.','bn':'আপনাকে ডাকা হচ্ছে! এখনই যান।','mr':'तुम्हाला बोलावले जात आहे! आत्ता जा.'},
    'select_dept':     {'en':'Select Department','hi':'विभाग चुनें','fr':'Choisir un Département','es':'Seleccionar Departamento','de':'Abteilung wählen','de':'Abteilung auswählen','ar':'اختر القسم','bn':'বিভাগ নির্বাচন করুন','mr':'विभाग निवडा'},
    'select_doctor':   {'en':'Select Doctor','hi':'डॉक्टर चुनें','fr':'Choisir un Médecin','es':'Seleccionar Médico','de':'Arzt auswählen','ar':'اختر الطبيب','bn':'ডাক্তার নির্বাচন করুন','mr':'डॉक्टर निवडा'},
    'confirm_token':   {'en':'Confirm & Get Token','hi':'पुष्टि करें और टोकन लें','fr':'Confirmer et Obtenir','es':'Confirmar y Obtener','de':'Bestätigen und Token holen','ar':'تأكيد والحصول على الرقم','bn':'নিশ্চিত করুন এবং টোকেন নিন','mr':'पुष्टी करा आणि टोकन मिळवा'},

    # ── FORMS ─────────────────────────────────────────────────────────────────
    'full_name':       {'en':'Full Name','hi':'पूरा नाम','fr':'Nom Complet','es':'Nombre Completo','de':'Vollständiger Name','ar':'الاسم الكامل','bn':'পুরো নাম','mr':'पूर्ण नाव'},
    'email':           {'en':'Email','hi':'ईमेल','fr':'Email','es':'Correo Electrónico','de':'E-Mail','ar':'البريد الإلكتروني','bn':'ইমেইল','mr':'ईमेल'},
    'password':        {'en':'Password','hi':'पासवर्ड','fr':'Mot de passe','es':'Contraseña','de':'Passwort','ar':'كلمة المرور','bn':'পাসওয়ার্ড','mr':'पासवर्ड'},
    'age':             {'en':'Age','hi':'आयु','fr':'Âge','es':'Edad','de':'Alter','ar':'العمر','bn':'বয়স','mr':'वय'},
    'gender':          {'en':'Gender','hi':'लिंग','fr':'Genre','es':'Género','de':'Geschlecht','ar':'الجنس','bn':'লিঙ্গ','mr':'लिंग'},
    'phone':           {'en':'Phone','hi':'फ़ोन','fr':'Téléphone','es':'Teléfono','de':'Telefon','ar':'الهاتف','bn':'ফোন','mr':'फोन'},
    'city':            {'en':'City','hi':'शहर','fr':'Ville','es':'Ciudad','de':'Stadt','ar':'المدينة','bn':'শহর','mr':'शहर'},
    'blood_group':     {'en':'Blood Group','hi':'रक्त समूह','fr':'Groupe Sanguin','es':'Grupo Sanguíneo','de':'Blutgruppe','ar':'فصيلة الدم','bn':'রক্তের গ্রুপ','mr':'रक्त गट'},
    'create_account':  {'en':'Create Account →','hi':'खाता बनाएं →','fr':'Créer un compte →','es':'Crear cuenta →','de':'Konto erstellen →','ar':'إنشاء حساب →','bn':'অ্যাকাউন্ট তৈরি করুন →','mr':'खाते तयार करा →'},
    'already_account': {'en':'Already have an account?','hi':'पहले से खाता है?','fr':'Déjà un compte?','es':'¿Ya tiene una cuenta?','de':'Bereits ein Konto?','ar':'هل لديك حساب؟','bn':'ইতিমধ্যে একটি অ্যাকাউন্ট আছে?','mr':'आधीच खाते आहे?'},
    'login_here':      {'en':'Login here','hi':'यहाँ लॉगिन करें','fr':'Connectez-vous ici','es':'Inicia sesión aquí','de':'Hier anmelden','ar':'سجل الدخول هنا','bn':'এখানে লগইন করুন','mr':'येथे लॉगिन करा'},
    'no_account':      {'en':'New patient?','hi':'नए मरीज़?','fr':'Nouveau patient?','es':'¿Nuevo paciente?','de':'Neuer Patient?','ar':'مريض جديد؟','bn':'নতুন রোগী?','mr':'नवीन रुग्ण?'},

    # ── DOCTOR ────────────────────────────────────────────────────────────────
    'doctor_portal':   {'en':'Doctor Portal','hi':'डॉक्टर पोर्टल','fr':'Portail Médecin','es':'Portal Médico','de':'Arztportal','ar':'بوابة الطبيب','bn':'ডাক্তার পোর্টাল','mr':'डॉक्टर पोर्टल'},
    'doctor_dashboard':{'en':'Doctor Dashboard','hi':'डॉक्टर डैशबोर्ड','fr':'Tableau de bord Médecin','es':'Panel del Médico','de':'Arzt-Dashboard','ar':'لوحة تحكم الطبيب','bn':'ডাক্তার ড্যাশবোর্ড','mr':'डॉक्टर डॅशबोर्ड'},
    'call_next':       {'en':'Call Next Patient','hi':'अगला मरीज़ बुलाएं','fr':'Appeler le prochain','es':'Llamar al siguiente','de':'Nächsten aufrufen','ar':'استدعاء المريض التالي','bn':'পরবর্তী রোগী ডাকুন','mr':'पुढील रुग्णाला बोलवा'},
    'mark_complete':   {'en':'Mark Completed','hi':'पूर्ण चिह्नित करें','fr':'Marquer terminé','es':'Marcar completado','de':'Als abgeschlossen markieren','ar':'وضع علامة مكتمل','bn':'সম্পন্ন চিহ্নিত করুন','mr':'पूर्ण म्हणून चिन्हांकित करा'},
    'waiting_queue':   {'en':'Waiting Queue','hi':'प्रतीक्षा कतार','fr':'File d\'attente','es':'Cola de espera','de':'Warteschlange','ar':'قائمة الانتظار','bn':'অপেক্ষার কিউ','mr':'प्रतीक्षा रांग'},
    'currently_attending':{'en':'Currently Attending','hi':'वर्तमान में देख रहे हैं','fr':'En consultation','es':'Atendiendo actualmente','de':'Wird gerade behandelt','ar':'يُعالج حالياً','bn':'বর্তমানে পরিচর্যা করা হচ্ছে','mr':'सध्या तपासत आहे'},
    'add_record':      {'en':'Add Medical Record','hi':'मेडिकल रिकॉर्ड जोड़ें','fr':'Ajouter un dossier','es':'Agregar registro médico','de':'Medizinische Akte hinzufügen','ar':'إضافة سجل طبي','bn':'মেডিকেল রেকর্ড যোগ করুন','mr':'वैद्यकीय नोंद जोडा'},

    # ── AI FEATURES ───────────────────────────────────────────────────────────
    'symptom_checker': {'en':'AI Symptom Checker','hi':'AI लक्षण जाँचक','fr':'Vérificateur de Symptômes IA','es':'Verificador de Síntomas IA','de':'KI-Symptomprüfer','ar':'فاحص الأعراض بالذكاء الاصطناعي','bn':'এআই লক্ষণ পরীক্ষক','mr':'एआय लक्षण तपासक'},
    'medibot':         {'en':'MediBot Chat','hi':'MediBot चैट','fr':'Chat MediBot','es':'Chat MediBot','de':'MediBot-Chat','ar':'دردشة MediBot','bn':'মেডিবট চ্যাট','mr':'मेडिबॉट चॅट'},
    'describe_symptoms':{'en':'Describe your symptoms','hi':'अपने लक्षण बताएं','fr':'Décrivez vos symptômes','es':'Describa sus síntomas','de':'Beschreiben Sie Ihre Symptome','ar':'صف أعراضك','bn':'আপনার লক্ষণ বর্ণনা করুন','mr':'तुमची लक्षणे सांगा'},
    'analyse_ai':      {'en':'Analyse with AI','hi':'AI से विश्लेषण करें','fr':'Analyser avec IA','es':'Analizar con IA','de':'Mit KI analysieren','ar':'تحليل بالذكاء الاصطناعي','bn':'এআই দিয়ে বিশ্লেষণ করুন','mr':'एआयने विश्लेषण करा'},
    'ai_recommendation':{'en':'AI Recommendation','hi':'AI सुझाव','fr':'Recommandation IA','es':'Recomendación IA','de':'KI-Empfehlung','ar':'توصية الذكاء الاصطناعي','bn':'এআই সুপারিশ','mr':'एआय शिफारस'},

    # ── APPOINTMENTS ─────────────────────────────────────────────────────────
    'book_appointment':{'en':'Book Appointment','hi':'अपॉइंटमेंट बुक करें','fr':'Prendre rendez-vous','es':'Reservar cita','de':'Termin buchen','ar':'حجز موعد','bn':'অ্যাপয়েন্টমেন্ট বুক করুন','mr':'अपॉईंटमेंट बुक करा'},
    'appointments':    {'en':'Appointments','hi':'अपॉइंटमेंट','fr':'Rendez-vous','es':'Citas','de':'Termine','ar':'المواعيد','bn':'অ্যাপয়েন্টমেন্ট','mr':'अपॉईंटमेंट'},
    'medical_records': {'en':'Medical Records','hi':'मेडिकल रिकॉर्ड','fr':'Dossiers Médicaux','es':'Registros Médicos','de':'Medizinische Akten','ar':'السجلات الطبية','bn':'মেডিকেল রেকর্ড','mr':'वैद्यकीय नोंदी'},

    # ── COMMON ────────────────────────────────────────────────────────────────
    'save_changes':    {'en':'Save Changes','hi':'बदलाव सहेजें','fr':'Enregistrer','es':'Guardar cambios','de':'Änderungen speichern','ar':'حفظ التغييرات','bn':'পরিবর্তন সংরক্ষণ করুন','mr':'बदल जतन करा'},
    'cancel':          {'en':'Cancel','hi':'रद्द करें','fr':'Annuler','es':'Cancelar','de':'Abbrechen','ar':'إلغاء','bn':'বাতিল করুন','mr':'रद्द करा'},
    'back':            {'en':'Back','hi':'वापस','fr':'Retour','es':'Volver','de':'Zurück','ar':'رجوع','bn':'ফিরে যান','mr':'मागे'},
    'search':          {'en':'Search','hi':'खोजें','fr':'Rechercher','es':'Buscar','de':'Suchen','ar':'بحث','bn':'খুঁজুন','mr':'शोधा'},
    'department':      {'en':'Department','hi':'विभाग','fr':'Département','es':'Departamento','de':'Abteilung','ar':'القسم','bn':'বিভাग','mr':'विभाग'},
    'doctor':          {'en':'Doctor','hi':'डॉक्टर','fr':'Médecin','es':'Médico','de':'Arzt','ar':'الطبيب','bn':'ডাক্তার','mr':'डॉक्टर'},
    'patient':         {'en':'Patient','hi':'मरीज़','fr':'Patient','es':'Paciente','de':'Patient','ar':'المريض','bn':'রোগী','mr':'रुग्ण'},
    'status':          {'en':'Status','hi':'स्थिति','fr':'Statut','es':'Estado','de':'Status','ar':'الحالة','bn':'অবস্থা','mr':'स्थिती'},
    'date':            {'en':'Date','hi':'तारीख','fr':'Date','es':'Fecha','de':'Datum','ar':'التاريخ','bn':'তারিখ','mr':'तारीख'},
    'time':            {'en':'Time','hi':'समय','fr':'Heure','es':'Hora','de':'Uhrzeit','ar':'الوقت','bn':'সময়','mr':'वेळ'},
    'notes':           {'en':'Notes','hi':'नोट्स','fr':'Notes','es':'Notas','de':'Notizen','ar':'الملاحظات','bn':'নোট','mr':'टिपणी'},
    'token_history':   {'en':'Token History','hi':'टोकन इतिहास','fr':'Historique des numéros','es':'Historial de tokens','de':'Token-Verlauf','ar':'سجل الأرقام','bn':'টোকেন ইতিহাস','mr':'टोकन इतिहास'},
    'find_doctor':     {'en':'Find Doctor','hi':'डॉक्टर खोजें','fr':'Trouver un Médecin','es':'Buscar Médico','de':'Arzt finden','ar':'ابحث عن طبيب','bn':'ডাক্তার খুঁজুন','mr':'डॉक्टर शोधा'},
    'choose_language': {'en':'Language','hi':'भाषा','fr':'Langue','es':'Idioma','de':'Sprache','ar':'اللغة','bn':'ভাষা','mr':'भाषा'},
    'select':          {'en':'Select','hi':'चुनें','fr':'Sélectionner','es':'Seleccionar','de':'Auswählen','ar':'اختر','bn':'নির্বাচন করুন','mr':'निवडा'},
    'experience':      {'en':'Experience','hi':'अनुभव','fr':'Expérience','es':'Experiencia','de':'Erfahrung','ar':'الخبرة','bn':'অভিজ্ঞতা','mr':'अनुभव'},
    'qualification':   {'en':'Qualification','hi':'योग्यता','fr':'Qualification','es':'Calificación','de':'Qualifikation','ar':'المؤهل','bn':'যোগ্যতা','mr':'पात्रता'},
    'done_today':      {'en':'Done Today','hi':'आज पूर्ण','fr':'Fait aujourd\'hui','es':'Hecho hoy','de':'Heute erledigt','ar':'أُنجز اليوم','bn':'আজ সম্পন্ন','mr':'आज पूर्ण'},
    'in_session':      {'en':'In Session','hi':'सत्र में','fr':'En session','es':'En sesión','de':'In Sitzung','ar':'في الجلسة','bn':'সেশনে','mr':'सत्रात'},
    'mins':            {'en':'min','hi':'मिनट','fr':'min','es':'min','de':'Min','ar':'دقيقة','bn':'মিনিট','mr':'मिनिट'},
    'years':           {'en':'yrs','hi':'वर्ष','fr':'ans','es':'años','de':'Jahre','ar':'سنوات','bn':'বছর','mr':'वर्षे'},
    'no_queue':        {'en':'Queue is empty! Great work.','hi':'कतार खाली है! बढ़िया काम।','fr':'File vide! Bon travail.','es':'¡Cola vacía! Buen trabajo.','de':'Warteschlange leer! Gute Arbeit.','ar':'قائمة الانتظار فارغة! عمل رائع.','bn':'কিউ খালি! দারুণ কাজ।','mr':'रांग रिकामी आहे! छान काम.'},
    'ai_disclaimer':   {'en':'AI suggestion only. Always consult a qualified doctor.','hi':'केवल AI सुझाव। हमेशा योग्य डॉक्टर से सलाह लें।','fr':'Suggestion IA uniquement. Consultez toujours un médecin.','es':'Solo sugerencia de IA. Siempre consulte a un médico.','de':'Nur KI-Vorschlag. Immer einen Arzt aufsuchen.','ar':'اقتراح الذكاء الاصطناعي فقط. استشر دائمًا طبيبًا مؤهلاً.','bn':'শুধুমাত্র এআই পরামর্শ। সর্বদা একজন যোগ্য ডাক্তারের সাথে পরামর্শ করুন।','mr':'फक्त एआय सूचना. नेहमी पात्र डॉक्टरांचा सल्ला घ्या.'},

    # ── EMAIL NOTIFICATIONS ───────────────────────────────────────────────────
    'email_token_subject':   {'en':'Token #{} Generated — SmartQueue Hospital','hi':'टोकन #{} बना — SmartQueue हॉस्पिटल','fr':'Numéro #{} généré — SmartQueue Hôpital','es':'Número #{} generado — SmartQueue Hospital','de':'Token #{} erstellt — SmartQueue Krankenhaus','ar':'تم إنشاء الرقم #{} — مستشفى SmartQueue','bn':'টোকেন #{} তৈরি হয়েছে — SmartQueue হাসপাতাল','mr':'टोकन #{} तयार — SmartQueue रुग्णालय'},
    'email_called_subject':  {'en':'Token #{} Called — Please Come Now!','hi':'टोकन #{} बुलाया — अभी आएं!','fr':'Numéro #{} appelé — Venez maintenant!','es':'¡Número #{} llamado — Venga ahora!','de':'Token #{} aufgerufen — Bitte kommen Sie jetzt!','ar':'تم استدعاء الرقم #{} — تعال الآن!','bn':'টোকেন #{} ডাকা হয়েছে — এখনই আসুন!','mr':'टोकन #{} बोलावले — आत्ता या!'},
    'email_complete_subject':{'en':'Visit Completed — Thank You!','hi':'भेट पूर्ण — धन्यवाद!','fr':'Visite terminée — Merci!','es':'Visita completada — ¡Gracias!','de':'Besuch abgeschlossen — Danke!','ar':'اكتملت الزيارة — شكراً!','bn':'পরিদর্শন সম্পন্ন — ধন্যবাদ!','mr':'भेट पूर्ण — धन्यवाद!'},
    'email_token_ready':     {'en':'Your Token is Ready!','hi':'आपका टोकन तैयार है!','fr':'Votre numéro est prêt!','es':'¡Su número está listo!','de':'Ihr Token ist fertig!','ar':'رقمك جاهز!','bn':'আপনার টোকেন প্রস্তুত!','mr':'तुमचा टोकन तयार आहे!'},
    'email_your_turn':       {'en':'Your Turn Has Come!','hi':'आपकी बारी आ गई!','fr':'C\'est votre tour!','es':'¡Es su turno!','de':'Sie sind dran!','ar':'حان دورك!','bn':'আপনার পালা এসেছে!','mr':'तुमची वेळ आली!'},
    'email_visit_done':      {'en':'Visit Completed!','hi':'भेट पूर्ण!','fr':'Visite terminée!','es':'¡Visita completada!','de':'Besuch abgeschlossen!','ar':'اكتملت الزيارة!','bn':'পরিদর্শন সম্পন্ন!','mr':'भेट पूर्ण!'},
    'email_dear':            {'en':'Dear','hi':'प्रिय','fr':'Cher/Chère','es':'Estimado/a','de':'Liebe/r','ar':'عزيزي','bn':'প্রিয়','mr':'प्रिय'},
    'email_token_body':      {'en':'Your queue token has been generated successfully.','hi':'आपका कतार टोकन सफलतापूर्वक बना दिया गया है।','fr':'Votre numéro de file d\'attente a été généré.','es':'Su número de cola ha sido generado exitosamente.','de':'Ihr Warteschlangen-Token wurde erfolgreich erstellt.','ar':'تم إنشاء رقم الانتظار الخاص بك بنجاح.','bn':'আপনার কিউ টোকেন সফলভাবে তৈরি হয়েছে।','mr':'तुमचा रांग टोकन यशस्वीरित्या तयार झाला आहे.'},
    'email_token_number':    {'en':'Your Token Number','hi':'आपका टोकन नंबर','fr':'Votre numéro','es':'Su número','de':'Ihre Token-Nummer','ar':'رقم تذكرتك','bn':'আপনার টোকেন নম্বর','mr':'तुमचा टोकन नंबर'},
    'email_stay_nearby':     {'en':'Please stay nearby and wait for your token to be called.','hi':'कृपया पास रहें और अपने टोकन के बुलाए जाने का इंतज़ार करें।','fr':'Veuillez rester à proximité et attendre que votre numéro soit appelé.','es':'Permanezca cerca y espere que llamen su número.','de':'Bitte bleiben Sie in der Nähe und warten Sie, bis Ihr Token aufgerufen wird.','ar':'يرجى البقاء قريبًا وانتظار استدعاء رقمك.','bn':'অনুগ্রহ করে কাছাকাছি থাকুন এবং আপনার টোকেন ডাকার জন্য অপেক্ষা করুন।','mr':'कृपया जवळ रहा आणि टोकन बोलावण्याची प्रतीक्षा करा.'},
    'email_proceed_now':     {'en':'Please proceed to the doctor\'s room immediately.','hi':'कृपया तुरंत डॉक्टर के कमरे में जाएं।','fr':'Veuillez vous rendre immédiatement dans la salle du médecin.','es':'Por favor, diríjase inmediatamente a la consulta del médico.','de':'Bitte begeben Sie sich sofort in das Arztzimmer.','ar':'يرجى التوجه فورًا إلى غرفة الطبيب.','bn':'অনুগ্রহ করে অবিলম্বে ডাক্তারের কক্ষে যান।','mr':'कृपया ताबडतोब डॉक्टरांच्या खोलीत जा.'},
    'email_dont_miss':       {'en':'If you don\'t appear within 5 minutes, your token may be skipped.','hi':'यदि आप 5 मिनट में नहीं आए, तो आपका टोकन छोड़ा जा सकता है।','fr':'Si vous ne vous présentez pas dans 5 minutes, votre numéro peut être annulé.','es':'Si no aparece en 5 minutos, su número puede ser omitido.','de':'Wenn Sie nicht innerhalb von 5 Minuten erscheinen, kann Ihr Token übersprungen werden.','ar':'إذا لم تحضر خلال 5 دقائق، فقد يتم تخطي رقمك.','bn':'যদি ৫ মিনিটের মধ্যে না আসেন, আপনার টোকেন বাদ দেওয়া হতে পারে।','mr':'५ मिनिटांत न आल्यास तुमचा टोकन वगळला जाऊ शकतो.'},
    'email_visit_thanks':    {'en':'Thank you for visiting SmartQueue Hospital. We hope you feel better soon!','hi':'SmartQueue हॉस्पिटल में आने के लिए धन्यवाद। जल्द स्वस्थ हों!','fr':'Merci pour votre visite. Nous vous souhaitons un prompt rétablissement!','es':'Gracias por visitar SmartQueue Hospital. ¡Esperamos que se recupere pronto!','de':'Vielen Dank für Ihren Besuch. Gute Besserung!','ar':'شكرًا لزيارة مستشفى SmartQueue. نتمنى لك الشفاء العاجل!','bn':'SmartQueue হাসপাতালে আসার জন্য ধন্যবাদ। শীঘ্রই সুস্থ হয়ে উঠুন!','mr':'SmartQueue रुग्णालयाला भेट दिल्याबद्दल धन्यवाद. लवकर बरे व्हा!'},
    'email_get_well':        {'en':'Get well soon! 💚','hi':'जल्दी ठीक हो जाओ! 💚','fr':'Rétablissez-vous vite! 💚','es':'¡Que te mejores pronto! 💚','de':'Gute Besserung! 💚','ar':'الشفاء العاجل! 💚','bn':'শীঘ্রই সুস্থ হন! 💚','mr':'लवकर बरे व्हा! 💚'},
    'email_follow_advice':   {'en':'Please follow the doctor\'s advice and take your medicines on time.','hi':'कृपया डॉक्टर की सलाह मानें और समय पर दवाएं लें।','fr':'Veuillez suivre les conseils du médecin et prendre vos médicaments à temps.','es':'Siga los consejos del médico y tome sus medicamentos a tiempo.','de':'Bitte folgen Sie dem Rat des Arztes und nehmen Sie Ihre Medikamente rechtzeitig.','ar':'يرجى اتباع نصيحة الطبيب وتناول أدويتك في الوقت المحدد.','bn':'অনুগ্রহ করে ডাক্তারের পরামর্শ অনুসরণ করুন এবং সময়মতো ওষুধ নিন।','mr':'कृपया डॉक्टरांचा सल्ला पाळा आणि वेळेवर औषधे घ्या.'},

    # ── FORGOT PASSWORD ──────────────────────────────────────────────────────
    'forgot_password':   {'en':'Forgot Password','hi':'पासवर्ड भूल गए'},
    'forgot_subtitle':   {'en':'Enter your email to receive an OTP','hi':'OTP पाने के लिए अपना ईमेल दर्ज करें'},
    'send_otp':          {'en':'Send OTP →','hi':'OTP भेजें →'},
    'enter_otp':         {'en':'Enter OTP','hi':'OTP दर्ज करें'},
    'otp_sent_msg':      {'en':'A 6-digit OTP has been sent to your email.','hi':'आपके ईमेल पर 6 अंकों का OTP भेजा गया है।'},
    'otp_placeholder':   {'en':'Enter 6-digit OTP','hi':'6 अंकों का OTP दर्ज करें'},
    'verify_otp':        {'en':'Verify OTP →','hi':'OTP सत्यापित करें →'},
    'new_password':      {'en':'New Password','hi':'नया पासवर्ड'},
    'confirm_password':  {'en':'Confirm Password','hi':'पासवर्ड की पुष्टि करें'},
    'reset_password':    {'en':'Reset Password →','hi':'पासवर्ड रीसेट करें →'},
    'back_to_login':     {'en':'Back to Login','hi':'लॉगिन पर वापस जाएं'},
    'otp_expired':       {'en':'OTP expired. Please request a new one.','hi':'OTP समाप्त हो गया। नया OTP मांगें।'},
    'otp_invalid':       {'en':'Invalid OTP. Please try again.','hi':'गलत OTP। कृपया पुनः प्रयास करें।'},
    'email_not_found':   {'en':'Email not registered. Please check and try again.','hi':'ईमेल पंजीकृत नहीं है। कृपया जांचें और पुनः प्रयास करें।'},
    'pwd_reset_success': {'en':'Password reset successfully! Please login.','hi':'पासवर्ड सफलतापूर्वक रीसेट हुआ! कृपया लॉगिन करें।'},
    'pwd_mismatch':      {'en':'Passwords do not match.','hi':'पासवर्ड मेल नहीं खाते।'},
    'otp_resend':        {'en':'Resend OTP','hi':'OTP दोबारा भेजें'},
    'check_email':       {'en':'Check your email','hi':'अपना ईमेल जांचें'},
    'otp_expires_in':    {'en':'OTP expires in 10 minutes','hi':'OTP 10 मिनट में समाप्त होगा'},

    # ── OTP LOGIN BY MOBILE ───────────────────────────────────────────────────
    'login_with_otp':    {'en':'Login with Mobile OTP','hi':'मोबाइल OTP से लॉगिन'},
    'mobile_otp_sub':    {'en':'Enter your registered mobile number','hi':'अपना पंजीकृत मोबाइल नंबर दर्ज करें'},
    'mobile_number':     {'en':'Mobile Number','hi':'मोबाइल नंबर'},
    'mobile_placeholder':{'en':'Enter 10-digit mobile number','hi':'10 अंकों का मोबाइल नंबर दर्ज करें'},
    'send_mobile_otp':   {'en':'Send OTP to Mobile','hi':'मोबाइल पर OTP भेजें'},
    'mobile_otp_note':   {'en':'OTP will be sent to your registered email (linked to this mobile number)','hi':'OTP आपके पंजीकृत ईमेल पर भेजा जाएगा (इस मोबाइल नंबर से जुड़ा)'},
    'mobile_not_found':  {'en':'Mobile number not registered. Please register first.','hi':'मोबाइल नंबर पंजीकृत नहीं है। पहले रजिस्टर करें।'},
    'or_divider':        {'en':'OR','hi':'या'},
    'login_with_email':  {'en':'Login with Email & Password','hi':'ईमेल और पासवर्ड से लॉगिन'},

    # ── EMAIL OTP TEMPLATES ───────────────────────────────────────────────────
    'otp_email_subject': {'en':'Your SmartQueue OTP Code','hi':'आपका SmartQueue OTP कोड'},
    'otp_email_title':   {'en':'Your One-Time Password','hi':'आपका एक बार का पासवर्ड'},
    'otp_email_body':    {'en':'Use the following OTP to proceed. It is valid for 10 minutes.','hi':'आगे बढ़ने के लिए निम्नलिखित OTP का उपयोग करें। यह 10 मिनट के लिए वैध है।'},
    'otp_email_warning': {'en':'Do not share this OTP with anyone.','hi':'यह OTP किसी के साथ साझा न करें।'},
    'otp_email_ignore':  {'en':'If you did not request this, please ignore this email.','hi':'यदि आपने यह नहीं मांगा, तो इस ईमेल को अनदेखा करें।'},
    # ── MISSING DASHBOARD KEYS ────────────────────────────────────────────────
    'ai_symptom_checker':  {'en':'AI Symptom Checker','hi':'AI लक्षण जाँचक','fr':'Vérificateur IA','es':'Verificador IA','de':'KI-Symptomprüfer','ar':'فاحص الأعراض','bn':'এআই লক্ষণ পরীক্ষক','mr':'एआय लक्षण तपासक'},
    'medibot_chat':        {'en':'MediBot Chat','hi':'MediBot चैट','fr':'Chat MediBot','es':'Chat MediBot','de':'MediBot-Chat','ar':'دردشة MediBot','bn':'মেডিবট চ্যাট','mr':'मेडिबॉट चॅट'},
    'ai_feature':          {'en':'AI Feature','hi':'AI सुविधा','fr':'Fonctionnalité IA','es':'Función IA','de':'KI-Funktion','ar':'ميزة الذكاء الاصطناعي','bn':'এআই ফিচার','mr':'एआय वैशिष्ट्य'},
    'symptoms_ai_desc':    {'en':'Describe symptoms → AI picks department','hi':'लक्षण बताएं → AI विभाग चुनेगा','fr':'Décrivez → IA choisit le département','es':'Síntomas → IA elige departamento','de':'Symptome → KI wählt Abteilung','ar':'الأعراض → الذكاء الاصطناعي يختار','bn':'লক্ষণ → এআই বিভাগ বেছে নেয়','mr':'लक्षणे → एआय विभाग निवडतो'},
    'medibot_desc':        {'en':'Ask any health question anytime','hi':'कभी भी स्वास्थ्य प्रश्न पूछें','fr':'Posez des questions santé','es':'Haga preguntas de salud','de':'Gesundheitsfragen stellen','ar':'اسأل أي سؤال صحي','bn':'যেকোনো স্বাস্থ্য প্রশ্ন করুন','mr':'कोणताही आरोग्य प्रश्न विचारा'},
    'step1_dept':          {'en':'Step 1 — Select Department','hi':'चरण 1 — विभाग चुनें','fr':'Étape 1 — Choisir département','es':'Paso 1 — Seleccionar departamento','de':'Schritt 1 — Abteilung wählen','ar':'الخطوة 1 — اختر القسم','bn':'ধাপ ১ — বিভাগ নির্বাচন করুন','mr':'पायरी १ — विभाग निवडा'},
    'step2_doctor':        {'en':'Step 2 — Select Doctor','hi':'चरण 2 — डॉक्टर चुनें','fr':'Étape 2 — Choisir médecin','es':'Paso 2 — Seleccionar médico','de':'Schritt 2 — Arzt wählen','ar':'الخطوة 2 — اختر الطبيب','bn':'ধাপ ২ — ডাক্তার নির্বাচন করুন','mr':'पायरी २ — डॉक्टर निवडा'},
    'use_ai_dept':         {'en':'Not sure? Use AI','hi':'निश्चित नहीं? AI उपयोग करें','fr':'Pas sûr? Utiliser IA','es':'¿No está seguro? Use IA','de':'Unsicher? KI verwenden','ar':'غير متأكد؟ استخدم الذكاء الاصطناعي','bn':'নিশ্চিত নন? এআই ব্যবহার করুন','mr':'खात्री नाही? एआय वापरा'},
    'change_dept':         {'en':'← Change dept','hi':'← विभाग बदलें','fr':'← Changer dept','es':'← Cambiar dept','de':'← Abteilung ändern','ar':'← تغيير القسم','bn':'← বিভাগ পরিবর্তন করুন','mr':'← विभाग बदला'},
    'selected':            {'en':'Selected','hi':'चुना गया','fr':'Sélectionné','es':'Seleccionado','de':'Ausgewählt','ar':'المحدد','bn':'নির্বাচিত','mr':'निवडले'},
    'reset':               {'en':'Reset','hi':'रीसेट','fr':'Réinitialiser','es':'Restablecer','de':'Zurücksetzen','ar':'إعادة تعيين','bn':'রিসেট','mr':'रीसेट'},
    'available_doctors':   {'en':'Available Doctors','hi':'उपलब्ध डॉक्टर','fr':'Médecins disponibles','es':'Médicos disponibles','de':'Verfügbare Ärzte','ar':'الأطباء المتاحون','bn':'উপলব্ধ ডাক্তার','mr':'उपलब्ध डॉक्टर'},
    'my_appointments':     {'en':'My Appointments','hi':'मेरी अपॉइंटमेंट','fr':'Mes rendez-vous','es':'Mis citas','de':'Meine Termine','ar':'مواعيدي','bn':'আমার অ্যাপয়েন্টমেন্ট','mr':'माझ्या अपॉईंटमेंट'},
    'my_records':          {'en':'My Records','hi':'मेरे रिकॉर्ड','fr':'Mes dossiers','es':'Mis registros','de':'Meine Akten','ar':'سجلاتي','bn':'আমার রেকর্ড','mr':'माझ्या नोंदी'},
    'token_number':        {'en':'Token Number','hi':'टोकन नंबर','fr':'Numéro de ticket','es':'Número de turno','de':'Token-Nummer','ar':'رقم التذكرة','bn':'টোকেন নম্বর','mr':'टोकन क्रमांक'},
    'book_new_appt':       {'en':'+ Book New Appointment','hi':'+ नई अपॉइंटमेंट बुक करें','fr':'+ Nouveau rendez-vous','es':'+ Nueva cita','de':'+ Neuen Termin buchen','ar':'+ حجز موعد جديد','bn':'+ নতুন অ্যাপয়েন্টমেন্ট বুক করুন','mr':'+ नवीन अपॉईंटमेंट बुक करा'},
    'no_active_token':     {'en':'No active token','hi':'कोई सक्रिय टोकन नहीं','fr':'Aucun ticket actif','es':'Sin turno activo','de':'Kein aktiver Token','ar':'لا توجد تذكرة نشطة','bn':'কোনো সক্রিয় টোকেন নেই','mr':'कोणताही सक्रिय टोकन नाही'},
    'no_appointments':     {'en':'No appointments yet','hi':'अभी कोई अपॉइंटमेंट नहीं','fr':"Aucun rendez-vous",'es':'Sin citas aún','de':'Noch keine Termine','ar':'لا مواعيد بعد','bn':'এখনো কোনো অ্যাপয়েন্টমেন্ট নেই','mr':'अजून कोणतीही अपॉईंटमेंट नाही'},
    'no_records':          {'en':'No records yet','hi':'अभी कोई रिकॉर्ड नहीं','fr':'Aucun dossier','es':'Sin registros','de':'Noch keine Akten','ar':'لا سجلات بعد','bn':'এখনো কোনো রেকর্ড নেই','mr':'अजून कोणतीही नोंद नाही'},
    'no_tokens':           {'en':'No tokens yet','hi':'अभी कोई टोकन नहीं','fr':'Aucun ticket','es':'Sin tokens','de':'Noch keine Token','ar':'لا أرقام بعد','bn':'এখনো কোনো টোকেন নেই','mr':'अजून कोणताही टोकन नाही'},
    'display_board':       {'en':'Display Board','hi':'डिस्प्ले बोर्ड','fr':"Tableau d'affichage",'es':'Panel de pantalla','de':'Anzeigetafel','ar':'لوحة العرض','bn':'ডিসপ্লে বোর্ড','mr':'प्रदर्शन फलक'},
    'my_profile':          {'en':'My Profile','hi':'मेरी प्रोफ़ाइल','fr':'Mon profil','es':'Mi perfil','de':'Mein Profil','ar':'ملفي الشخصي','bn':'আমার প্রোফাইল','mr':'माझी प्रोफाइल'},
    'confirm_cancel':      {'en':'Cancel this appointment?','hi':'यह अपॉइंटमेंट रद्द करें?','fr':'Annuler ce rendez-vous?','es':'¿Cancelar esta cita?','de':'Diesen Termin absagen?','ar':'إلغاء هذا الموعد؟','bn':'এই অ্যাপয়েন্টমেন্ট বাতিল করবেন?','mr':'हे अपॉईंटमेंट रद्द करायचे?'},
    'diagnosis':           {'en':'Diagnosis','hi':'निदान','fr':'Diagnostic','es':'Diagnóstico','de':'Diagnose','ar':'التشخيص','bn':'রোগ নির্ণয়','mr':'निदान'},
    'medicines':           {'en':'Medicines','hi':'दवाइयाँ','fr':'Médicaments','es':'Medicamentos','de':'Medikamente','ar':'الأدوية','bn':'ওষুধ','mr':'औषधे'},
    'followup':            {'en':'Follow-up','hi':'फॉलो-अप','fr':'Suivi','es':'Seguimiento','de':'Nachsorge','ar':'المتابعة','bn':'ফলো-আপ','mr':'फॉलो-अप'},
    'search_doctor':       {'en':'Search doctor or specialty...','hi':'डॉक्टर या विशेषता खोजें...','fr':'Chercher médecin ou spécialité...','es':'Buscar médico o especialidad...','de':'Arzt oder Fachgebiet suchen...','ar':'ابحث عن طبيب أو تخصص...','bn':'ডাক্তার বা বিশেষত্ব খুঁজুন...','mr':'डॉक्टर किंवा विशेषता शोधा...'},
    'all_departments':     {'en':'All Departments','hi':'सभी विभाग','fr':'Tous les départements','es':'Todos los departamentos','de':'Alle Abteilungen','ar':'جميع الأقسام','bn':'সব বিভাগ','mr':'सर्व विभाग'},
    # Doctor dashboard
    'ai_queue_insights':   {'en':'AI Queue Insights','hi':'AI कतार अंतर्दृष्टि','fr':'Insights IA de file','es':'Perspectivas IA de cola','de':'KI-Warteschlangeneinblicke','ar':'رؤى الذكاء الاصطناعي للقائمة','bn':'এআই কিউ অন্তর্দৃষ্টি','mr':'एआय रांग अंतर्दृष्टी'},
    'get_insights':        {'en':'Get AI Insights','hi':'AI अंतर्दृष्टि पाएं','fr':'Obtenir insights IA','es':'Obtener perspectivas IA','de':'KI-Einblicke erhalten','ar':'احصل على رؤى الذكاء الاصطناعي','bn':'এআই অন্তর্দৃষ্টি পান','mr':'एआय अंतर्दृष्टी मिळवा'},
    'refresh_insights':    {'en':'Refresh Insights','hi':'अंतर्दृष्टि ताज़ा करें','fr':'Actualiser insights','es':'Actualizar perspectivas','de':'Einblicke aktualisieren','ar':'تحديث الرؤى','bn':'অন্তর্দৃষ্টি রিফ্রেশ করুন','mr':'अंतर्दृष्टी रिफ्रेश करा'},
    'click_for_insights':  {'en':'Click "Get AI Insights" to analyse your queue…','hi':'"AI अंतर्दृष्टि पाएं" क्लिक करें…','fr':'Cliquez pour analyser la file…','es':'Clic para analizar la cola…','de':'Klicken Sie für Einblicke…','ar':'انقر للحصول على رؤى الذكاء الاصطناعي…','bn':'"এআই অন্তর্দৃষ্টি পান" ক্লিক করুন…','mr':'"एआय अंतर्दृष्टी मिळवा" वर क्लिक करा…'},
    'currently_attending': {'en':'Currently Attending','hi':'वर्तमान में देख रहे हैं','fr':'En consultation','es':'Atendiendo actualmente','de':'Wird gerade behandelt','ar':'يُعالج حالياً','bn':'বর্তমানে পরিচর্যা','mr':'सध्या तपासत आहे'},
    'done_and_next':       {'en':'Done & Call Next','hi':'पूर्ण और अगला बुलाएं','fr':'Terminé et suivant','es':'Hecho y siguiente','de':'Fertig und nächster','ar':'تم واستدعاء التالي','bn':'সম্পন্ন ও পরবর্তী','mr':'पूर्ण आणि पुढील'},
    'no_session':          {'en':"No patient in session",'hi':'कोई मरीज़ नहीं','fr':'Aucun patient en session','es':'Sin paciente en sesión','de':'Kein Patient in Sitzung','ar':'لا يوجد مريض في الجلسة','bn':'সেশনে কোনো রোগী নেই','mr':'सत्रात कोणताही रुग्ण नाही'},
    'click_call_next':     {'en':"Click 'Call Next Patient' to begin",'hi':'"अगला मरीज़ बुलाएं" क्लिक करें','fr':'Cliquez pour commencer','es':'Clic para comenzar','de':'Klicken zum Starten','ar':'انقر لبدء الاستشارة','bn':'শুরু করতে ক্লিক করুন','mr':'सुरू करण्यासाठी क्लिक करा'},
    'todays_appointments': {'en':"Today's Appointments",'hi':'आज की अपॉइंटमेंट','fr':"Rendez-vous du jour",'es':'Citas de hoy','de':'Heutige Termine','ar':'مواعيد اليوم','bn':'আজকের অ্যাপয়েন্টমেন্ট','mr':'आजच्या अपॉईंटमेंट'},
    'recent_records':      {'en':'Recent Medical Records','hi':'हाल के मेडिकल रिकॉर्ड','fr':'Dossiers médicaux récents','es':'Registros médicos recientes','de':'Aktuelle medizinische Akten','ar':'السجلات الطبية الأخيرة','bn':'সাম্প্রতিক মেডিকেল রেকর্ড','mr':'अलीकडील वैद्यकीय नोंदी'},
    'queue_empty':         {'en':'Queue is empty! Great work.','hi':'कतार खाली है! शानदार काम।','fr':'File vide! Excellent travail.','es':'¡Cola vacía! Gran trabajo.','de':'Warteschlange leer! Gute Arbeit.','ar':'قائمة الانتظار فارغة! عمل رائع.','bn':'কিউ খালি! দারুণ কাজ।','mr':'रांग रिकामी! छान काम.'},
    'total_wait':          {'en':'Total Wait','hi':'कुल प्रतीक्षा','fr':'Attente totale','es':'Espera total','de':'Gesamtwartezeit','ar':'إجمالي وقت الانتظار','bn':'মোট অপেক্ষা','mr':'एकूण प्रतीक्षा'},
    # Display board
    'live_display':        {'en':'Live Token Display','hi':'लाइव टोकन डिस्प्ले','fr':'Affichage en direct','es':'Pantalla en vivo','de':'Live-Anzeige','ar':'عرض مباشر','bn':'লাইভ টোকেন ডিসপ্লে','mr':'लाइव्ह टोकन प्रदर्शन'},
    'now_serving':         {'en':'Now Serving','hi':'अभी सेवा में','fr':'En cours','es':'Atendiendo ahora','de':'Wird bedient','ar':'يُخدم الآن','bn':'এখন সেবা দেওয়া হচ্ছে','mr':'आता सेवा देत आहे'},
    'next_token':          {'en':'Next','hi':'अगला','fr':'Suivant','es':'Siguiente','de':'Nächster','ar':'التالي','bn':'পরবর্তী','mr':'पुढील'},
    'patients_waiting':    {'en':'patients waiting','hi':'मरीज़ प्रतीक्षा में','fr':'patients en attente','es':'pacientes esperando','de':'Patienten wartend','ar':'مرضى في الانتظار','bn':'রোগী অপেক্ষায়','mr':'रुग्ण प्रतीक्षेत'},
    # Notifications
    'notification_lang':   {'en':'Notification Language','hi':'अधिसूचना भाषा','fr':'Langue de notification','es':'Idioma de notificación','de':'Benachrichtigungssprache','ar':'لغة الإشعار','bn':'বিজ্ঞপ্তির ভাষা','mr':'सूचना भाषा'},
    'email_notif_lang':    {'en':'Email notifications will be sent in this language.','hi':'ईमेल सूचनाएं इस भाषा में भेजी जाएंगी।','fr':'Les notifications seront envoyées dans cette langue.','es':'Las notificaciones se enviarán en este idioma.','de':'E-Mail-Benachrichtigungen in dieser Sprache.','ar':'سيتم إرسال الإشعارات بهذه اللغة.','bn':'ইমেইল বিজ্ঞপ্তি এই ভাষায় পাঠানো হবে।','mr':'ईमेल सूचना या भाषेत पाठवल्या जातील.'},
    # ── TOKEN TIMESTAMP KEYS ──────────────────────────────────────────────────
    'generated':   {'en':'Generated','hi':'बनाया गया','fr':'Généré','es':'Generado','de':'Erstellt','ar':'تم الإنشاء','bn':'তৈরি হয়েছে','mr':'तयार झाले'},
    'meet_time':   {'en':'Est. Meet at','hi':'अनुमानित मिलने का समय','fr':'Heure de rencontre est.','es':'Hora estimada de reunión','de':'Geschätzte Treffzeit','ar':'وقت اللقاء المقدر','bn':'আনুমানিক সাক্ষাৎ সময়','mr':'अंदाजे भेटीची वेळ'},
    'token_gen_time': {'en':'Token Generated','hi':'टोकन बनाया गया','fr':'Ticket créé','es':'Turno generado','de':'Token erstellt','ar':'تم إنشاء التذكرة','bn':'টোকেন তৈরি','mr':'टोकन तयार'},
    'est_meet_time':  {'en':'Estimated Meeting Time','hi':'अनुमानित मिलने का समय','fr':'Heure estimée de consultation','es':'Hora estimada de consulta','de':'Geschätzte Konsultationszeit','ar':'الوقت المقدر للاستشارة','bn':'আনুমানিক পরামর্শের সময়','mr':'अंदाजे सल्लामसलतीची वेळ'},

}


def t(key, lang='en'):
    """Get translation for a key in given language."""
    entry = TRANSLATIONS.get(key, {})
    return entry.get(lang) or entry.get('en') or key


def get_lang():
    """Get current language from Flask session (imported inside function to avoid circular import)."""
    try:
        from flask import session
        return session.get('lang', 'en')
    except Exception:
        return 'en'
