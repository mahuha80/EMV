"""Content for index page + Lessons 1-2"""

INDEX_BODY = '''
<div class="info-box">
    <h3>👋 Chào mừng đến với EMV Academy</h3>
    <p>Khóa học này hướng dẫn bạn — một <strong>lập trình viên Android</strong> chưa có nền tảng về thanh toán — từng bước làm chủ chuẩn <strong>EMV</strong> (Europay-Mastercard-Visa): chuẩn toàn cầu cho thẻ thanh toán có chip mà gần như mọi POS, ATM, mobile wallet ngày nay đều tuân theo.</p>
    <p>Tài liệu tham chiếu chính: <strong>EMV Integrated Circuit Card Specifications for Payment Systems v4.4 (EMVCo)</strong>, gồm 4 quyển (Book 1-4) và <strong>EMV Contactless Specifications (kernel C-1 đến C-8)</strong>.</p>
</div>

<div class="stat-grid">
    <div class="stat-box"><div class="stat-value">10</div><div class="stat-label">Bài học</div></div>
    <div class="stat-box"><div class="stat-value">4</div><div class="stat-label">EMV Books tham chiếu</div></div>
    <div class="stat-box"><div class="stat-value">100%</div><div class="stat-label">Theo spec EMVCo</div></div>
    <div class="stat-box"><div class="stat-value">Kotlin</div><div class="stat-label">Code Android</div></div>
</div>

<div class="section">
    <h2>📚 Nội dung khóa học</h2>
    <div class="lesson-grid">
        <a href="lessons/lesson01.html" class="lesson-card">
            <span class="lesson-number">BÀI 01</span>
            <h3>EMV là gì?</h3>
            <p>Lịch sử, vai trò của EMVCo, so sánh chip vs magnetic stripe, contact vs contactless.</p>
        </a>
        <a href="lessons/lesson02.html" class="lesson-card">
            <span class="lesson-number">BÀI 02</span>
            <h3>Kiến trúc thẻ EMV</h3>
            <p>ISO/IEC 7816, ATR, file system (MF/DF/EF), AID, PSE/PPSE.</p>
        </a>
        <a href="lessons/lesson03.html" class="lesson-card">
            <span class="lesson-number">BÀI 03</span>
            <h3>Transaction Flow</h3>
            <p>8 bước transaction theo EMV Book 3, online vs offline, cryptogram (TC/ARQC/AAC).</p>
        </a>
        <a href="lessons/lesson04.html" class="lesson-card">
            <span class="lesson-number">BÀI 04</span>
            <h3>APDU Commands</h3>
            <p>ISO 7816-4: cấu trúc C-APDU/R-APDU, status words, SELECT/GPO/READ RECORD/GENERATE AC.</p>
        </a>
        <a href="lessons/lesson05.html" class="lesson-card">
            <span class="lesson-number">BÀI 05</span>
            <h3>BER-TLV & EMV Tags</h3>
            <p>Cấu trúc BER-TLV (ISO 7816-4 / ASN.1), tag encoding, danh sách tag EMV phổ biến.</p>
        </a>
        <a href="lessons/lesson06.html" class="lesson-card">
            <span class="lesson-number">BÀI 06</span>
            <h3>Cryptography trong EMV</h3>
            <p>RSA, 3DES, AES, SHA, MAC; key hierarchy CA / Issuer / ICC; session key.</p>
        </a>
        <a href="lessons/lesson07.html" class="lesson-card">
            <span class="lesson-number">BÀI 07</span>
            <h3>Offline Data Authentication</h3>
            <p>SDA, DDA, CDA — cơ chế chống clone thẻ, verify certificate chain.</p>
        </a>
        <a href="lessons/lesson08.html" class="lesson-card">
            <span class="lesson-number">BÀI 08</span>
            <h3>Android NFC + EMV</h3>
            <p>NfcAdapter, IsoDep, foreground dispatch, gửi APDU bằng Kotlin.</p>
        </a>
        <a href="lessons/lesson09.html" class="lesson-card">
            <span class="lesson-number">BÀI 09</span>
            <h3>Demo: Đọc thẻ thật</h3>
            <p>Project Android hoàn chỉnh: SELECT PPSE → SELECT AID → GPO → READ RECORD → parse TLV.</p>
        </a>
        <a href="lessons/lesson10.html" class="lesson-card">
            <span class="lesson-number">BÀI 10</span>
            <h3>Bảo mật & PCI DSS</h3>
            <p>PCI DSS v4.0, dữ liệu nào được/không được lưu, tokenization, best practices.</p>
        </a>
    </div>
</div>

<div class="section">
    <h2>🎯 Sau khóa học bạn sẽ</h2>
    <ul>
        <li>Hiểu rõ một giao dịch EMV diễn ra như thế nào, từ lúc chạm thẻ đến lúc nhận được approval từ ngân hàng.</li>
        <li>Đọc hiểu mọi APDU response của thẻ EMV (Visa, Mastercard, JCB, UnionPay…).</li>
        <li>Tự viết được Android app sử dụng NFC để đọc các thông tin <em>không nhạy cảm</em> trên thẻ.</li>
        <li>Biết được giới hạn pháp lý/PCI DSS: cái gì được phép, cái gì không.</li>
    </ul>
</div>

<div class="warning-box">
    <h3>⚠️ Tuyên bố pháp lý</h3>
    <p>Khóa học chỉ dành cho mục đích <strong>giáo dục</strong>. Mọi thao tác đọc thẻ phải thực hiện trên thẻ <strong>của chính bạn</strong>. Tuyệt đối không lưu trữ PAN đầy đủ, không cố gắng giải mã PIN/CVV — đây là vi phạm PCI DSS và luật pháp.</p>
</div>
'''


# ============================================================
# LESSON 1: EMV là gì?
# ============================================================
LESSON_01 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Giải thích EMV là gì, ai duy trì chuẩn này, và tại sao nó tồn tại.</li>
        <li>Hiểu sự khác biệt giữa thẻ từ (magnetic stripe) và thẻ chip EMV.</li>
        <li>Phân biệt 3 loại giao tiếp: contact (ISO 7816), contactless (ISO 14443), và mobile (HCE/Tokenization).</li>
        <li>Nắm các thuật ngữ nền tảng sẽ dùng trong toàn khóa.</li>
    </ul>
</div>

<div class="section">
    <h2>📖 EMV — định nghĩa chính xác</h2>
    <p><span class="keyword-highlight">EMV</span> là viết tắt của <strong>E</strong>uropay, <strong>M</strong>astercard, và <strong>V</strong>isa — ba tổ chức ban đầu cùng xây dựng chuẩn vào năm 1994. Hiện nay chuẩn được duy trì bởi <strong>EMVCo LLC</strong>, một tổ chức thuộc sở hữu của 6 thành viên: American Express, Discover, JCB, Mastercard, UnionPay, và Visa.</p>

    <p>EMV không phải một sản phẩm cụ thể, mà là <strong>tập hợp các specification</strong> mô tả:</p>
    <ul>
        <li>Cách chip trên thẻ giao tiếp với terminal (điện học, vật lý, giao thức APDU).</li>
        <li>Cách dữ liệu được tổ chức trong chip (file system, TLV).</li>
        <li>Cách xác thực thẻ và chủ thẻ (SDA/DDA/CDA, PIN, signature).</li>
        <li>Cách tạo và verify cryptogram để chống fraud.</li>
    </ul>

    <div class="info-box">
        <h3>💡 EMV vs EMVCo</h3>
        <p><strong>EMV</strong> = tên chuẩn. <strong>EMVCo</strong> = tổ chức duy trì chuẩn. Bạn sẽ thấy spec ghi “EMV Book 3, EMVCo 2023” — nghĩa là phiên bản 2023 của Book 3 do EMVCo công bố.</p>
    </div>
</div>

<div class="section">
    <h2>📜 Lịch sử — vì sao EMV ra đời</h2>
    <p>Trước EMV, gần như mọi thẻ thanh toán đều dùng <strong>magnetic stripe</strong> (dải từ ISO 7811). Dữ liệu thẻ (PAN, expiry, service code, CVV1) được mã hóa thành các bit từ tính cố định — và đây là tử huyệt:</p>

    <ul>
        <li>Dữ liệu <strong>tĩnh</strong>: chỉ cần đọc một lần là copy được toàn bộ thẻ.</li>
        <li>Skimming device giá vài chục USD có thể clone thẻ trong vài giây.</li>
        <li>Vào những năm 1990, fraud từ thẻ giả ở châu Âu lên hàng tỉ USD/năm.</li>
    </ul>

    <p>Năm 1994, Europay + Mastercard + Visa thống nhất viết chuẩn dùng <strong>smartcard chip</strong> theo ISO/IEC 7816 — một con chip nhỏ có CPU và bộ nhớ, có thể chạy crypto, tạo dữ liệu <em>động</em> cho mỗi giao dịch.</p>

    <table>
        <tr><th>Năm</th><th>Mốc</th></tr>
        <tr><td>1994</td><td>Europay, Mastercard, Visa thành lập EMVCo</td></tr>
        <tr><td>1996</td><td>EMV ’96 — phiên bản đầu tiên (v3.0)</td></tr>
        <tr><td>2000</td><td>EMV 4.0 — thêm contactless</td></tr>
        <tr><td>2004</td><td>EMV 4.1 — đa số ngân hàng EU triển khai</td></tr>
        <tr><td>2011</td><td>EMVCo mở rộng: thêm JCB, Amex, China UnionPay, Discover</td></tr>
        <tr><td>2015</td><td>Mỹ chính thức “liability shift” — bắt đầu chuyển đổi EMV</td></tr>
        <tr><td>2024</td><td>EMV 4.4 — bản hiện hành</td></tr>
    </table>

    <div class="info-box">
        <h3>📊 Hiệu quả EMV trong thực tế</h3>
        <p>Theo báo cáo Visa (2023), sau khi triển khai EMV, fraud tại các merchant chấp nhận chip ở Mỹ <strong>giảm 76%</strong> so với thời kỳ magnetic stripe. Tại Anh, fraud thẻ giảm từ £505 triệu (2008) xuống £47 triệu (2012) sau khi EMV phổ cập.</p>
    </div>
</div>

<div class="section">
    <h2>🆚 Magnetic Stripe vs EMV Chip</h2>

    <div class="payment-card">
        <div class="card-brand">VISA</div>
        <div class="card-chip"></div>
        <div class="card-number">4532 •••• •••• 9010</div>
        <div class="card-info">
            <div><span class="label">Cardholder</span>NGUYEN VAN A</div>
            <div><span class="label">Expires</span>12/27</div>
        </div>
    </div>

    <table>
        <tr><th>Tiêu chí</th><th>Magnetic Stripe</th><th>EMV Chip</th></tr>
        <tr><td>Chuẩn vật lý</td><td>ISO 7811</td><td>ISO/IEC 7816 (contact), ISO/IEC 14443 (contactless)</td></tr>
        <tr><td>Dung lượng</td><td>~226 byte (3 tracks)</td><td>8 KB – 144 KB EEPROM</td></tr>
        <tr><td>Bản chất dữ liệu</td><td>Tĩnh — copy được</td><td>Có khả năng tạo dữ liệu động (cryptogram)</td></tr>
        <tr><td>Cryptography</td><td>Không có</td><td>RSA, 3DES, AES, SHA</td></tr>
        <tr><td>Cardholder verification</td><td>Signature</td><td>Offline PIN, Online PIN, CDCVM, Signature, No CVM</td></tr>
        <tr><td>Chống clone</td><td>Rất khó</td><td>DDA/CDA gần như không thể clone (chip có private key trong secure element)</td></tr>
        <tr><td>Tốc độ giao dịch</td><td>~1s (swipe)</td><td>Contact: 1–3s; Contactless: &lt;500ms</td></tr>
    </table>

    <div class="warning-box">
        <h3>⚠️ Vì sao chip không thể clone?</h3>
        <p>Chip EMV có <strong>private key RSA</strong> (1024–2048 bit) được fuse cứng vào secure element ngay từ nhà máy. Không một câu lệnh APDU nào có thể đọc ra khóa này. Để giao dịch, chip <em>ký</em> dữ liệu bằng khóa, terminal <em>verify</em> bằng public key — kẻ tấn công nghe lén được signature cũng không tái tạo được khóa.</p>
    </div>
</div>

<div class="section">
    <h2>🔌 Ba kiểu giao tiếp</h2>

    <h3>1. Contact (Tiếp xúc) — ISO/IEC 7816</h3>
    <p>Thẻ phải được <strong>cắm</strong> vào reader. Reader cấp nguồn (Vcc 3V/5V) và clock cho chip qua 8 điểm tiếp xúc bằng vàng. Sau khi cấp nguồn, chip trả về <span class="keyword-highlight">ATR</span> (Answer To Reset) — chuỗi byte mô tả chip hỗ trợ giao thức nào (T=0 hoặc T=1), tốc độ baud, v.v.</p>

    <h3>2. Contactless (Không tiếp xúc) — ISO/IEC 14443</h3>
    <p>Thẻ chỉ cần <strong>chạm</strong> hoặc đưa lại gần (&lt;4 cm) reader. Truyền dữ liệu bằng sóng RF <strong>13.56 MHz</strong>. Chuẩn 14443 có hai biến thể: Type A (NXP Mifare, JCB, Visa payWave một số) và Type B (American Express ExpressPay, một số Visa). Sau khi thẻ "wake up" (REQA/REQB), kết nối được nâng lên giao thức APDU giống contact.</p>

    <h3>3. Mobile — HCE & Tokenization</h3>
    <p>Apple Pay / Google Pay không gửi PAN thật qua NFC. Thay vào đó, ngân hàng cấp một <strong>DPAN</strong> (Device PAN — một token 16 chữ số khác) cho thiết bị. Mỗi giao dịch tạo cryptogram bằng key của token, gửi qua mạng cùng DPAN. Token Service Provider (Visa Token Service, Mastercard MDES) sẽ map DPAN → PAN thật. Toàn bộ vẫn tuân chuẩn EMV (gọi là <em>EMV Payment Tokenisation Specification</em>).</p>

    <div class="info-box">
        <h3>📱 Vì sao Android có thể làm thẻ?</h3>
        <p>Android 4.4+ hỗ trợ <strong>HCE</strong> (Host Card Emulation). App của bạn đăng ký AID, khi user chạm POS, hệ thống route APDU từ POS lên app — app trả lời như một thẻ thật. Đây là cơ chế đằng sau Google Pay.</p>
    </div>
</div>

<div class="section">
    <h2>🏗️ Các bên trong một giao dịch EMV</h2>
    <div class="flow-step">
        <div class="step-number">1</div>
        <div class="step-content">
            <h4>Cardholder</h4>
            <p>Chủ thẻ — sở hữu thẻ và thực hiện giao dịch.</p>
        </div>
    </div>
    <div class="flow-step">
        <div class="step-number">2</div>
        <div class="step-content">
            <h4>Card / Token (ICC)</h4>
            <p><strong>ICC</strong> = Integrated Circuit Card. Chip có hệ điều hành (Java Card, MULTOS…), chứa các application Visa/Mastercard/…</p>
        </div>
    </div>
    <div class="flow-step">
        <div class="step-number">3</div>
        <div class="step-content">
            <h4>Terminal (POS/ATM)</h4>
            <p>Thiết bị chấp nhận thẻ. Chạy phần mềm gọi là <strong>EMV kernel</strong> (mỗi network có kernel riêng: Visa = Kernel 3, Mastercard = Kernel 2…).</p>
        </div>
    </div>
    <div class="flow-step">
        <div class="step-number">4</div>
        <div class="step-content">
            <h4>Acquirer</h4>
            <p>Ngân hàng của merchant. Nhận yêu cầu authorization từ POS, route đến network.</p>
        </div>
    </div>
    <div class="flow-step">
        <div class="step-number">5</div>
        <div class="step-content">
            <h4>Payment Network</h4>
            <p>Visa/Mastercard/JCB/UnionPay/Amex. Là “xa lộ” trung gian giữa acquirer và issuer.</p>
        </div>
    </div>
    <div class="flow-step">
        <div class="step-number">6</div>
        <div class="step-content">
            <h4>Issuer</h4>
            <p>Ngân hàng phát hành thẻ. Là bên cuối cùng quyết định approve/decline dựa trên số dư, hạn mức, cryptogram.</p>
        </div>
    </div>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>EMV</dt>
        <dd>Tập specification mô tả chuẩn giao tiếp giữa chip thẻ và terminal, do EMVCo phát hành.</dd>

        <dt>EMVCo</dt>
        <dd>Tổ chức (LLC) đồng sở hữu bởi Amex, Discover, JCB, Mastercard, UnionPay, Visa, duy trì spec EMV.</dd>

        <dt>ICC</dt>
        <dd>Integrated Circuit Card — thuật ngữ chính thức của chip thẻ trong spec.</dd>

        <dt>ATR</dt>
        <dd>Answer To Reset — chuỗi byte chip trả về ngay sau khi được cấp nguồn (contact card), mô tả khả năng của chip. Định nghĩa ở ISO/IEC 7816-3.</dd>

        <dt>PAN</dt>
        <dd>Primary Account Number — số thẻ (thường 13–19 chữ số), tag EMV <code>5A</code>.</dd>

        <dt>HCE</dt>
        <dd>Host Card Emulation — cơ chế của Android cho phép app đóng vai trò một thẻ contactless.</dd>

        <dt>Tokenization</dt>
        <dd>Thay PAN thật bằng một số khác (token / DPAN) trong quá trình thanh toán, nhằm bảo vệ PAN thật. Chuẩn: <em>EMV Payment Tokenisation Specification</em>.</dd>

        <dt>Kernel</dt>
        <dd>Phần mềm trên terminal thực thi flow EMV. Mỗi network có một hoặc nhiều kernel: C-2 (Mastercard PayPass), C-3 (Visa payWave), C-4 (Amex), C-5 (JCB), C-6 (Discover), C-7 (UnionPay).</dd>

        <dt>Issuer / Acquirer</dt>
        <dd>Issuer = ngân hàng phát hành thẻ. Acquirer = ngân hàng của merchant.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Mở ví của bạn, đếm xem có bao nhiêu thẻ. Thẻ nào có chip vàng, thẻ nào chỉ có dải từ?</li>
        <li>Tìm biểu tượng sóng wifi nằm ngang )))) trên thẻ — đó là chỉ báo thẻ contactless.</li>
        <li>Tra cứu: ngân hàng phát hành thẻ của bạn là issuer của network nào (Visa, Mastercard, JCB, NAPAS)?</li>
        <li>Đọc nhanh EMVCo Book 1 mục “Scope” (free download tại emvco.com) để làm quen ngôn ngữ spec.</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>EMV là tập specification (do EMVCo phát hành) chuẩn hóa giao tiếp giữa chip thẻ và terminal.</li>
        <li>Ra đời 1994 để chống fraud của thẻ từ; hiện đã trở thành chuẩn toàn cầu.</li>
        <li>Có 3 hình thức giao tiếp: contact (ISO 7816), contactless (ISO 14443), mobile (HCE + Tokenization).</li>
        <li>Một giao dịch có 6 vai trò: cardholder, card, terminal, acquirer, network, issuer.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 2: Kiến trúc thẻ EMV
# ============================================================
LESSON_02 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu kiến trúc phần cứng và phần mềm của một chip EMV.</li>
        <li>Hiểu file system theo ISO/IEC 7816-4: MF, DF, EF.</li>
        <li>Phân biệt AID, RID, PIX và biết AID của các network lớn.</li>
        <li>Hiểu vai trò của PSE và PPSE trong việc application selection.</li>
    </ul>
</div>

<div class="section">
    <h2>🔬 Phần cứng chip</h2>
    <p>Chip EMV thực chất là một <strong>microcontroller</strong> (gọi là <em>secure microcontroller</em> hay <em>secure element</em>), thường được sản xuất bởi NXP, Infineon, STMicroelectronics, Samsung, IDEMIA. Cấu trúc điển hình:</p>

    <table>
        <tr><th>Khối</th><th>Vai trò</th><th>Dung lượng tham khảo</th></tr>
        <tr><td>CPU</td><td>Thực thi OS và application (Java Card / MULTOS)</td><td>8-bit, 16-bit hoặc 32-bit ARM SC000/SC300</td></tr>
        <tr><td>ROM</td><td>Chứa OS, không thay đổi được</td><td>128 – 512 KB</td></tr>
        <tr><td>EEPROM / Flash</td><td>Chứa application và dữ liệu cá nhân hóa</td><td>72 – 144 KB</td></tr>
        <tr><td>RAM</td><td>Bộ nhớ làm việc tạm thời</td><td>4 – 16 KB</td></tr>
        <tr><td>Crypto co-processor</td><td>Tăng tốc RSA, AES, DES, SHA, ECC</td><td>RSA tới 4096-bit, ECC tới 521-bit</td></tr>
        <tr><td>True RNG</td><td>Tạo số ngẫu nhiên cho cryptogram</td><td>Hardware-based</td></tr>
    </table>

    <div class="info-box">
        <h3>🔐 Vì sao gọi là "secure element"?</h3>
        <p>Chip được thiết kế chống tấn công vật lý: side-channel (đo điện năng, đo thời gian), fault injection (laser, glitch điện áp), micro-probing. Sản phẩm phải được chứng nhận <strong>Common Criteria EAL4+ / EAL5+</strong> hoặc <strong>EMVCo Security Evaluation</strong> trước khi được phép phát hành thẻ thật.</p>
    </div>
</div>

<div class="section">
    <h2>💿 ATR — Answer To Reset</h2>
    <p>Với contact card, ngay sau khi terminal cấp nguồn (reset), chip phải gửi về <strong>ATR</strong> trong vòng 400 – 40000 clock cycle (ISO/IEC 7816-3). ATR mô tả: chip dùng giao thức T=0 hay T=1, tốc độ, mã quốc gia của nhà sản xuất…</p>

    <div class="code-block"><span class="comment">// Ví dụ ATR thực tế của một thẻ Visa contact</span>
<span class="hex">3B 6E 00 00 80 31 80 66 B0 84 0C 01 6E 01 83 00 90 00</span>

<span class="comment">// Phân rã:</span>
3B            <span class="comment">// TS  - direct convention</span>
6E            <span class="comment">// T0  - có TB1, TC1, TD1, và 14 byte historical</span>
00 00         <span class="comment">// TB1, TC1</span>
80            <span class="comment">// TD1 - giao thức T=0</span>
31 80 66 B0 84 0C 01 6E 01 83 00 90 00  <span class="comment">// Historical bytes (chứa thông tin chip)</span></div>

    <p>Với contactless, không có ATR mà có <strong>ATS</strong> (Answer To Select, ISO 14443-4) — tương tự nhưng cho RF.</p>
</div>

<div class="section">
    <h2>📁 File system (ISO/IEC 7816-4)</h2>
    <p>Bên trong chip, dữ liệu được tổ chức theo <strong>file system phân cấp</strong> giống như Unix:</p>

    <h3>Ba loại file</h3>
    <table>
        <tr><th>Loại</th><th>Tên đầy đủ</th><th>Tương tự Unix</th><th>Mô tả</th></tr>
        <tr><td><strong>MF</strong></td><td>Master File</td><td><code>/</code> (root)</td><td>File gốc, mỗi chip có đúng 1 MF. File ID cố định <code>3F00</code>.</td></tr>
        <tr><td><strong>DF</strong></td><td>Dedicated File</td><td>Folder</td><td>Thư mục chứa application. Mỗi DF có một AID để chọn nó.</td></tr>
        <tr><td><strong>EF</strong></td><td>Elementary File</td><td>File</td><td>File chứa dữ liệu thực. Có 4 cấu trúc: Transparent, Linear Fixed, Linear Variable, Cyclic.</td></tr>
        <tr><td><strong>ADF</strong></td><td>Application DF</td><td>Folder app</td><td>DF đặc biệt — chứa toàn bộ một payment application (Visa, Mastercard…).</td></tr>
    </table>

    <h3>SFI — Short File Identifier</h3>
    <p><span class="keyword-highlight">SFI</span> là số 1–30 (5 bit) dùng để tham chiếu một EF <em>bên trong</em> ADF hiện hành mà không cần đường dẫn đầy đủ. EMV dùng SFI rất nhiều: mọi file dữ liệu của application đều được locate bằng <code>(SFI, record number)</code>.</p>

    <div class="diagram"><pre>
                          ┌─────────────────┐
                          │  MF (3F00)      │
                          │   /             │
                          └────────┬────────┘
            ┌──────────────────────┼──────────────────────┐
            ▼                      ▼                      ▼
   ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
   │  DF: PSE       │    │  ADF: Visa     │    │  ADF: MC       │
   │  1PAY.SYS.DDF01│    │ A0000000031010 │    │ A0000000041010 │
   └────────┬───────┘    └────────┬───────┘    └────────┬───────┘
            │                      │                      │
            ▼                      ▼                      ▼
        EF (FCI            EFs (SFI 1-30):           EFs (SFI 1-30):
        Directory)         - PAN, Expiry              - PAN, Expiry
                           - CVM List                 - CVM List
                           - Card keys                - Card keys
                           - Transaction log          - Transaction log
    </pre></div>
</div>

<div class="section">
    <h2>🆔 AID — Application Identifier</h2>
    <p>Mỗi payment application trên chip có một <strong>AID</strong> dài 5–16 byte (theo ISO/IEC 7816-5).</p>

    <div class="code-block"><span class="comment">// Cấu trúc AID = RID (5 byte) + PIX (0 – 11 byte)</span>

<span class="hex">A0 00 00 00 03</span>  <span class="hex">10 10</span>
└─── RID ────┘  └─PIX─┘
   Visa Inc.    Credit/Debit</div>

    <h3>RID — Registered Application Provider Identifier</h3>
    <p>5 byte, cấp bởi ISO. Mỗi tổ chức payment có một RID:</p>

    <table>
        <tr><th>RID</th><th>Tổ chức</th></tr>
        <tr><td><code>A000000003</code></td><td>Visa International</td></tr>
        <tr><td><code>A000000004</code></td><td>Mastercard International</td></tr>
        <tr><td><code>A000000025</code></td><td>American Express</td></tr>
        <tr><td><code>A000000065</code></td><td>JCB Co., Ltd.</td></tr>
        <tr><td><code>A000000152</code></td><td>Discover Financial Services</td></tr>
        <tr><td><code>A000000333</code></td><td>China UnionPay</td></tr>
        <tr><td><code>A000000524</code></td><td>NAPAS (Việt Nam)</td></tr>
    </table>

    <h3>PIX — Proprietary Application Identifier Extension</h3>
    <p>0–11 byte do mỗi tổ chức tự định nghĩa, dùng để phân biệt sản phẩm.</p>

    <h3>AID của các sản phẩm phổ biến</h3>
    <table>
        <tr><th>AID</th><th>Application</th></tr>
        <tr><td><code>A0000000031010</code></td><td>Visa Credit or Debit</td></tr>
        <tr><td><code>A0000000032010</code></td><td>Visa Electron</td></tr>
        <tr><td><code>A0000000033010</code></td><td>Visa Interlink</td></tr>
        <tr><td><code>A0000000038010</code></td><td>Visa Plus</td></tr>
        <tr><td><code>A0000000041010</code></td><td>Mastercard Credit or Debit</td></tr>
        <tr><td><code>A0000000043060</code></td><td>Maestro</td></tr>
        <tr><td><code>A00000002501</code></td><td>American Express</td></tr>
        <tr><td><code>A0000000651010</code></td><td>JCB</td></tr>
        <tr><td><code>A000000333010101</code></td><td>UnionPay Debit</td></tr>
        <tr><td><code>A000000333010102</code></td><td>UnionPay Credit</td></tr>
        <tr><td><code>A0000005241010</code></td><td>NAPAS (thẻ chip nội địa Việt Nam)</td></tr>
    </table>

    <div class="warning-box">
        <h3>⚠️ Một thẻ có thể chứa nhiều AID</h3>
        <p>Thẻ "dual interface" của Vietcombank chẳng hạn có thể chứa cùng lúc <code>A0000000031010</code> (Visa) và <code>A0000005241010</code> (NAPAS) — terminal tự chọn cái phù hợp dựa trên priority.</p>
    </div>
</div>

<div class="section">
    <h2>📚 PSE & PPSE — Cơ chế Application Selection</h2>

    <h3>PSE — Payment System Environment (contact)</h3>
    <p>Theo EMV Book 1, mọi thẻ contact phải chứa một DF tên là <strong>PSE</strong> với DF Name cố định:</p>
    <div class="code-block">DF Name (ASCII):  <span class="string">"1PAY.SYS.DDF01"</span>
DF Name (hex):    <span class="hex">31 50 41 59 2E 53 59 53 2E 44 44 46 30 31</span>  <span class="comment">// 14 byte</span></div>

    <p>Bên trong PSE là một EF tên là “Payment System Directory” (SFI 1, mặc định) chứa <strong>danh sách AID</strong> mà thẻ hỗ trợ, kèm priority và label.</p>

    <h3>PPSE — Proximity Payment System Environment (contactless)</h3>
    <p>Tương đương với PSE nhưng cho contactless. DF Name:</p>
    <div class="code-block">DF Name (ASCII):  <span class="string">"2PAY.SYS.DDF01"</span>
DF Name (hex):    <span class="hex">32 50 41 59 2E 53 59 53 2E 44 44 46 30 31</span>  <span class="comment">// 14 byte</span></div>

    <p>Đây là <em>điểm bắt đầu</em> của mọi giao dịch contactless: terminal gửi <code>SELECT 2PAY.SYS.DDF01</code> để hỏi thẻ “bạn có những app nào?”.</p>

    <div class="info-box">
        <h3>🔢 ASCII → hex như nào?</h3>
        <p>Mỗi ký tự ASCII chiếm 1 byte. Ví dụ: '1' = <code>0x31</code>, 'P' = <code>0x50</code>, 'A' = <code>0x41</code>, 'Y' = <code>0x59</code>, '.' = <code>0x2E</code>. Bạn có thể verify bằng lệnh <code>echo -n "1PAY.SYS.DDF01" | xxd</code>.</p>
    </div>
</div>

<div class="section">
    <h2>🗂️ Dữ liệu trong một ADF</h2>
    <p>Khi terminal SELECT một AID (ví dụ <code>A0000000031010</code>), thẻ trả về <strong>FCI</strong> (File Control Information) gồm:</p>
    <ul>
        <li><code>50</code> Application Label — tên hiển thị: "VISA CREDIT"</li>
        <li><code>87</code> Application Priority Indicator</li>
        <li><code>5F2D</code> Language Preference</li>
        <li><code>9F12</code> Application Preferred Name</li>
        <li><code>9F38</code> PDOL — Processing Options Data Object List (danh sách dữ liệu terminal phải gửi trong GPO ở bước sau)</li>
    </ul>

    <p>Các EF chứa dữ liệu cá nhân hóa (PAN, expiry, CVM list, key…) được locate bằng <strong>AFL</strong> (Application File Locator, tag <code>94</code>) trả về sau lệnh GPO ở bài 3.</p>

    <div class="term-box">
        <h3>📘 Thuật ngữ bài này</h3>
        <dl>
            <dt>MF / DF / EF / ADF</dt>
            <dd>Master File / Dedicated File / Elementary File / Application DF — theo ISO/IEC 7816-4.</dd>

            <dt>SFI</dt>
            <dd>Short File Identifier — số 1–30 tham chiếu EF trong ADF hiện hành.</dd>

            <dt>ATR / ATS</dt>
            <dd>Answer To Reset (contact, ISO 7816-3) / Answer To Select (contactless, ISO 14443-4).</dd>

            <dt>AID</dt>
            <dd>Application Identifier — 5–16 byte định danh application. = RID + PIX.</dd>

            <dt>RID</dt>
            <dd>Registered Application Provider Identifier — 5 byte do ISO cấp.</dd>

            <dt>PIX</dt>
            <dd>Proprietary Identifier Extension — 0–11 byte do provider tự định nghĩa.</dd>

            <dt>PSE</dt>
            <dd>Payment System Environment — DF với DF Name "1PAY.SYS.DDF01", cho contact.</dd>

            <dt>PPSE</dt>
            <dd>Proximity Payment System Environment — DF với DF Name "2PAY.SYS.DDF01", cho contactless. Là entry point của mọi giao dịch tap-to-pay.</dd>

            <dt>FCI</dt>
            <dd>File Control Information — template <code>6F</code> chứa metadata của DF/ADF, trả về trong R-APDU của SELECT.</dd>

            <dt>PDOL</dt>
            <dd>Processing Options Data Object List — tag <code>9F38</code> trong FCI, liệt kê các tag mà terminal phải gửi trong lệnh GPO.</dd>
        </dl>
    </div>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Chuyển chuỗi "2PAY.SYS.DDF01" sang hex (bạn sẽ dùng nó rất nhiều ở các bài sau).</li>
        <li>Giải mã AID <code>A0000000043060</code> — đó là application gì? (gợi ý: tra bảng RID + PIX).</li>
        <li>Vẽ file tree cho một thẻ chứa cả Visa và NAPAS.</li>
        <li>Tải EMV Book 1 phần “Application Selection” (mục 12), đọc lướt để thấy spec mô tả PPSE chính xác như thế nào.</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>Chip EMV là secure microcontroller có CPU, ROM, EEPROM, RAM, crypto co-processor.</li>
        <li>Dữ liệu tổ chức theo file system ISO 7816-4: MF → DF/ADF → EF, EF được tham chiếu bằng SFI.</li>
        <li>Mỗi application có AID = RID (5 byte do ISO cấp) + PIX (do provider định nghĩa).</li>
        <li>PSE ("1PAY.SYS.DDF01") cho contact, PPSE ("2PAY.SYS.DDF01") cho contactless — là entry point để terminal liệt kê AID có sẵn.</li>
    </ul>
</div>
'''

