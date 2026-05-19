"""Content for Lessons 6-10"""

# ============================================================
# LESSON 6: Cryptography trong EMV
# ============================================================
LESSON_06 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu vai trò RSA, 3DES, AES, SHA trong EMV (theo EMV Book 2).</li>
        <li>Nắm key hierarchy: CA Key → Issuer Key → ICC Key.</li>
        <li>Hiểu cách card sinh Application Cryptogram (MAC ISO 9797-1 Algorithm 3).</li>
        <li>Hiểu derive session key (EMV Common Session Key Derivation).</li>
    </ul>
</div>

<div class="section">
    <h2>🔐 Tổng quan crypto trong EMV</h2>
    <table>
        <tr><th>Thuật toán</th><th>Loại</th><th>Dùng cho</th><th>Spec tham chiếu</th></tr>
        <tr><td>RSA</td><td>Public-key</td><td>Card authentication (SDA/DDA/CDA), encipher offline PIN, issuer authentication</td><td>EMV Book 2 §5–7; PKCS#1</td></tr>
        <tr><td>3DES (TDEA)</td><td>Symmetric</td><td>Application Cryptogram (TC/ARQC/AAC), MAC, derive session key</td><td>EMV Book 2 §8; ISO 9797-1 Alg 3</td></tr>
        <tr><td>AES</td><td>Symmetric</td><td>Thay thế 3DES trên các deployment mới (EMV Book 2 v4.4)</td><td>EMV Book 2 §8</td></tr>
        <tr><td>SHA-1 / SHA-256</td><td>Hash</td><td>Hash dữ liệu trước khi ký RSA, integrity check</td><td>FIPS 180-4</td></tr>
    </table>

    <div class="warning-box">
        <h3>⚠️ SHA-1 và RSA-1024 còn dùng không?</h3>
        <p>Trong EMV hiện tại <em>vẫn còn</em> SHA-1 (vì legacy card phát hành trước 2017). EMVCo bắt đầu deprecate: EMV Book 2 v4.4 ưu tiên SHA-256 và RSA-2048 cho key mới. Riêng dải <strong>RSA-1408 và 1984</strong> tồn tại trong spec để bridge — đừng ngạc nhiên khi thấy.</p>
    </div>
</div>

<div class="section">
    <h2>🌳 Key hierarchy</h2>
    <div class="diagram"><pre>
                ┌─────────────────────────────────┐
                │   CA (Certification Authority)  │
                │   - Public Key index: 1 byte    │  EMV Book 2 §11
                │   - RSA 1024/1408/1984/2048-bit │
                │   Khóa CA do mỗi NETWORK quản lý│  (Visa CA, Mastercard CA…)
                │   Public key được cài cứng vào  │
                │   mọi POS/Terminal              │
                └───────────────┬─────────────────┘
                                │ ký (sign)
                                ▼
                ┌─────────────────────────────────┐
                │   Issuer Public Key Certificate │  tag 90
                │   - Do CA ký                    │
                │   - Issuer = NGÂN HÀNG          │
                └───────────────┬─────────────────┘
                                │ ký
                                ▼
                ┌─────────────────────────────────┐
                │   ICC Public Key Certificate    │  tag 9F46
                │   - Do Issuer ký                │
                │   - ICC = chip cụ thể           │
                │   - Private key tương ứng nằm   │
                │     trong secure element, KHÔNG │
                │     thể xuất ra ngoài           │
                └─────────────────────────────────┘
    </pre></div>

    <h3>Verify certificate chain (terminal làm)</h3>
    <ol>
        <li>Đọc <strong>CA Public Key Index</strong> (tag <code>8F</code>) từ card → terminal tra trong bảng CA keys (cài sẵn) để lấy CA Public Key.</li>
        <li>Recover <strong>Issuer Public Key Certificate</strong> (tag <code>90</code>) bằng CA Public Key. Verify hash, expiry, PAN range.</li>
        <li>Recover <strong>ICC Public Key Certificate</strong> (tag <code>9F46</code>) bằng Issuer Public Key. Verify hash, PAN của certificate khớp PAN của card.</li>
        <li>Bây giờ terminal đã có ICC Public Key, dùng cho DDA/CDA.</li>
    </ol>

    <div class="info-box">
        <h3>📥 Bạn có thể tải CA public key thật</h3>
        <p>Mỗi network công bố CA public key. Ví dụ: <a href="https://www.eftlab.com/knowledge-base/list-of-ca-public-keys">eftlab.com</a> tổng hợp tất cả 200+ CA keys (Visa, Mastercard, JCB, Amex…). Bạn không cần khôi phục chúng từ đâu — chỉ cài vào terminal.</p>
    </div>
</div>

<div class="section">
    <h2>🔒 RSA trong EMV — chữ ký số</h2>
    <p>EMV dùng RSA theo <strong>ISO/IEC 9796-2 Scheme 1</strong> (message recovery). Khác PKCS#1 ở chỗ chữ ký <em>chứa cả</em> message — chỉ một phần message phải gửi riêng.</p>

    <div class="code-block"><span class="comment">// Chữ ký S được tạo bởi card:</span>
S = (Header || M1 || hash(M1 || M2) || Trailer)^d  mod n

<span class="comment">// Trong đó:</span>
<span class="comment">// Header   = 6A    (1 byte cố định)</span>
<span class="comment">// M1       = phần message được recover (tối đa N - 22 byte)</span>
<span class="comment">// hash     = SHA-1 hoặc SHA-256 trên (M1 || M2)</span>
<span class="comment">// Trailer  = BC (nếu SHA-1) hoặc khác (xem ISO 9796-2 §9.3)</span>
<span class="comment">// d, n     = private key, modulus của card</span>

<span class="comment">// Terminal verify:</span>
recovered = S^e mod n
<span class="comment">// Kiểm tra header 6A, trailer BC, hash khớp với hash(M1 || M2)</span></div>

    <h3>Vì sao dùng ISO 9796-2?</h3>
    <ul>
        <li>Recover một phần message → tiết kiệm băng thông (thẻ chỉ trả về phần "remainder" tag <code>92</code>).</li>
        <li>Thiết kế phù hợp cho thiết bị có RAM nhỏ.</li>
    </ul>
</div>

<div class="section">
    <h2>🔑 3DES (TDEA) — đối xứng</h2>
    <p>EMV dùng 3DES cho việc tạo MAC (cryptogram). Variant: <strong>2-key 3DES</strong> (16 byte key = K1‖K2, K3 = K1). Thuật toán: <strong>ISO/IEC 9797-1 MAC Algorithm 3</strong> với padding method 1 hoặc 2.</p>

    <div class="diagram"><pre>
Input data D, key K = K1‖K2 (16 byte)

D pad → D1 D2 ... Dn  (mỗi block 8 byte)

      D1                D2                       Dn
       │                 │                        │
       ▼                 ▼                        ▼
  ┌──DES(K1)───┐  ┌───XOR──┐  ┌───XOR──┐    ┌───XOR──┐
  │  H1        │  │  H1⊕D2 │  │  H2⊕D3 │ …  │ Hn-1⊕Dn│
  └─────┬──────┘  └────┬───┘  └────┬───┘    └────┬───┘
        ▼              ▼            ▼              ▼
                 DES(K1)         DES(K1)        DES(K1)
                                                     │
                                                     ▼
                                              DES⁻¹(K2)
                                                     │
                                                     ▼
                                              DES(K1) → MAC (8 byte)
    </pre></div>
</div>

<div class="section">
    <h2>🎫 Application Cryptogram (TC/ARQC/AAC)</h2>

    <h3>1. Master Key tại Issuer</h3>
    <p>Issuer giữ <strong>IMK_AC</strong> (Issuer Master Key for Application Cryptogram) — 16 byte. Đây là bí mật <em>chỉ Issuer biết</em>.</p>

    <h3>2. Derive UDK (Unique Derived Key) khi cá nhân hóa thẻ</h3>
    <p>EMV Book 2 §8.1.1 ("Common Card Master Key derivation"):</p>
    <div class="code-block">Y = PAN || PSN          <span class="comment">// nếu &lt; 16 nibble, pad bên trái bằng 0; sau đó lấy 16 nibble cuối = 8 byte</span>

UDK_L = 3DES_Encrypt(IMK_AC, Y)
UDK_R = 3DES_Encrypt(IMK_AC, Y XOR 0xFFFFFFFFFFFFFFFF)
UDK   = UDK_L || UDK_R            <span class="comment">// 16 byte, cá nhân hóa vào chip</span></div>

    <h3>3. Derive Session Key khi giao dịch (EMV CSK)</h3>
    <p>EMV Book 2 §8.1.3 ("Common Session Key Derivation"):</p>
    <div class="code-block">F1 = ATC || "F0 00 00 00 00 00"   <span class="comment">// 8 byte</span>
F2 = ATC || "0F 00 00 00 00 00"

SK_L = 3DES_Encrypt(UDK, F1)
SK_R = 3DES_Encrypt(UDK, F2)
SK_AC = SK_L || SK_R              <span class="comment">// session key cho giao dịch này</span></div>

    <h3>4. Tính Application Cryptogram</h3>
    <div class="code-block">data = CDOL1_data || AIP || ATC || IAD_input
AC   = MAC_3DES(SK_AC, data) [first 8 bytes]</div>

    <h3>5. Issuer verify ARQC</h3>
    <ol>
        <li>Issuer nhận ARQC + ATC + PAN + CDOL1 + AIP + IAD qua message ISO 8583 (DE 55).</li>
        <li>Tái tạo UDK từ IMK_AC + PAN/PSN.</li>
        <li>Tái tạo SK_AC từ UDK + ATC.</li>
        <li>Tính lại MAC, so sánh với ARQC nhận được.</li>
    </ol>

    <div class="info-box">
        <h3>💡 Vì sao phải có UN và ATC?</h3>
        <p><strong>ATC</strong> đảm bảo session key luôn khác, ngay cả khi cùng amount → chống <em>replay attack</em>. <strong>UN</strong> (Unpredictable Number) đảm bảo terminal challenge khác nhau → chống <em>pre-computed attack</em>.</p>
    </div>
</div>

<div class="section">
    <h2>↩️ ARPC — Issuer ký phản hồi</h2>
    <p>Sau khi verify ARQC, issuer sinh <strong>ARPC</strong> (Authorization Response Cryptogram) gửi xuống terminal để card verify. Đảm bảo response thật sự đến từ issuer.</p>

    <h3>ARPC Method 1 (EMV Book 2 §8.2.1)</h3>
    <div class="code-block">ARPC = 3DES_Encrypt(SK_AC, ARQC XOR (ARC || "00 00 00 00 00 00"))</div>
    <p>(ARC = Authorization Response Code, ví dụ "00" → 0x3030)</p>

    <h3>ARPC Method 2 (CSU-based, dùng từ EMV 4.2)</h3>
    <p>Sử dụng <strong>CSU</strong> (Card Status Update, 4 byte) + Proprietary Auth Data, MAC bằng 3DES — phép truyền tải nhiều thông điệp hơn về phía card.</p>
</div>

<div class="section">
    <h2>🔐 Offline PIN encryption (RSA)</h2>
    <p>Khi CVM yêu cầu <em>enciphered offline PIN</em>, terminal phải lấy được <strong>ICC PIN Encipherment Public Key</strong> (tag <code>9F2D / 9F2E / 9F2F</code>) — có thể cùng key với DDA hoặc khác. Sau đó:</p>

    <div class="code-block">PIN_block_format2 = 2 || L || PIN_digits || pad_F
random_bytes      = N - 17 byte ngẫu nhiên                <span class="comment">// N = key size byte</span>
plaintext         = 7F || PIN_block || random_bytes || 01  <span class="comment">// header 7F, trailer BC</span>

ciphertext = RSA_Encrypt(plaintext, ICC_PIN_PK)            <span class="comment">// dùng public key</span>
&gt;&gt; <span class="hex">00 20 00 88 Lc [ciphertext]</span>                <span class="comment">// VERIFY P2 = 88 = enciphered</span></div>

    <p>Chỉ card mới giải mã được (vì chỉ card có private key tương ứng), so sánh với PIN nội bộ.</p>
</div>

<div class="section">
    <h2>📱 Kotlin — 3DES MAC theo ISO 9797-1 Alg 3</h2>
    <div class="code-block">import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.IvParameterSpec

fun mac3desRetail(key16: ByteArray, data: ByteArray): ByteArray {
    require(key16.size == 16)
    val k1 = key16.copyOfRange(0, 8)
    val k2 = key16.copyOfRange(8, 16)

    val padded = isoPad1(data)               <span class="comment">// padding method 1: pad bằng 0x00</span>
    var h = ByteArray(8)

    <span class="comment">// 1) DES-CBC với K1 trên tất cả block trừ block cuối</span>
    val desK1 = Cipher.getInstance("DES/CBC/NoPadding").apply {
        init(Cipher.ENCRYPT_MODE, SecretKeySpec(k1, "DES"), IvParameterSpec(ByteArray(8)))
    }
    var i = 0
    while (i &lt; padded.size - 8) {
        h = desK1.doFinal(padded.copyOfRange(i, i + 8))
        desK1.init(Cipher.ENCRYPT_MODE, SecretKeySpec(k1, "DES"), IvParameterSpec(h))
        i += 8
    }

    <span class="comment">// 2) Block cuối: XOR h, sau đó 3DES (encrypt-K1, decrypt-K2, encrypt-K1)</span>
    val last = xor(padded.copyOfRange(i, i + 8), h)
    val e1 = Cipher.getInstance("DES/ECB/NoPadding").apply {
        init(Cipher.ENCRYPT_MODE, SecretKeySpec(k1, "DES"))
    }.doFinal(last)
    val d2 = Cipher.getInstance("DES/ECB/NoPadding").apply {
        init(Cipher.DECRYPT_MODE, SecretKeySpec(k2, "DES"))
    }.doFinal(e1)
    val e3 = Cipher.getInstance("DES/ECB/NoPadding").apply {
        init(Cipher.ENCRYPT_MODE, SecretKeySpec(k1, "DES"))
    }.doFinal(d2)
    return e3
}

fun xor(a: ByteArray, b: ByteArray) =
    ByteArray(a.size) { i -&gt; (a[i].toInt() xor b[i].toInt()).toByte() }

fun isoPad1(data: ByteArray): ByteArray {
    val padLen = 8 - (data.size % 8)
    return if (padLen == 8) data else data + ByteArray(padLen)
}</div>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>IMK / UDK / SK</dt>
        <dd>Issuer Master Key / Unique Derived Key (per card) / Session Key (per transaction).</dd>
        <dt>CA Public Key</dt>
        <dd>Khóa công khai của Network (Visa CA, MC CA…). Mỗi key có một <em>index</em> 1 byte. Terminal cài tất cả CA keys.</dd>
        <dt>ARC</dt>
        <dd>Authorization Response Code — 2 ký tự ASCII issuer trả về (00, 01, 05, 91…).</dd>
        <dt>ARPC</dt>
        <dd>Authorization Response Cryptogram — chữ ký của issuer trên ARQC + ARC.</dd>
        <dt>ISO 9797-1 MAC Algorithm 3</dt>
        <dd>Thuật toán MAC dựa DES-CBC + 3DES cho block cuối ("retail MAC"). EMV dùng cho AC.</dd>
        <dt>ISO 9796-2 Scheme 1</dt>
        <dd>RSA signature scheme với message recovery — EMV dùng cho mọi chữ ký số (Issuer cert, ICC cert, SDAD).</dd>
        <dt>SHA-1 / SHA-256</dt>
        <dd>Hash 160/256-bit theo FIPS 180-4. EMV dùng để tạo digest trước khi RSA-sign.</dd>
        <dt>PIN Block Format 2</dt>
        <dd>Format dùng cho offline PIN giữa terminal và ICC, theo ISO 9564-1.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Cho IMK = 16 byte số 0, PAN = 4532123456789010, PSN = 00. Tính UDK (dùng OpenSSL CLI hoặc code Kotlin).</li>
        <li>Cho UDK ở câu 1, ATC = 0x001A. Tính SK_AC.</li>
        <li>SHA-1 vs SHA-256: số byte output bao nhiêu?</li>
        <li>Vì sao ICC private key không bao giờ rời chip?</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>EMV dùng RSA (theo ISO 9796-2) cho authentication, 3DES/AES (theo ISO 9797-1 Alg 3) cho cryptogram.</li>
        <li>Key hierarchy: CA → Issuer Cert (tag 90) → ICC Cert (tag 9F46). Terminal verify chuỗi này.</li>
        <li>UDK derive từ IMK + PAN/PSN; SK_AC derive từ UDK + ATC mỗi giao dịch.</li>
        <li>ARQC do card sinh, issuer verify; ARPC do issuer sinh, card verify.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 7: Offline Data Authentication
# ============================================================
LESSON_07 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu vì sao có Offline Data Authentication (ODA).</li>
        <li>Phân biệt SDA, DDA, CDA và biết khi nào nào dùng cái nào.</li>
        <li>Biết các tag liên quan (<code>8F</code>, <code>90</code>, <code>92</code>, <code>93</code>, <code>9F46–9F4B</code>).</li>
        <li>Vẽ được flow verify certificate chain.</li>
    </ul>
</div>

<div class="section">
    <h2>❓ Vấn đề ODA giải quyết</h2>
    <p>Khi giao dịch <strong>offline</strong> (không gọi online tới issuer), terminal cần một cách để chắc chắn:</p>
    <ol>
        <li>Dữ liệu đọc từ thẻ <em>không bị giả mạo</em>.</li>
        <li>Thẻ <em>thật sự là thẻ ngân hàng phát hành</em>, không phải clone.</li>
    </ol>
    <p>ODA = cơ chế chữ ký RSA chứng minh hai điều trên, do EMV Book 2 §5–7 định nghĩa. Có 3 cấp độ:</p>

    <table>
        <tr><th>Method</th><th>Chống tampering data?</th><th>Chống clone?</th><th>Bit b8/b6/b1 AIP</th></tr>
        <tr><td><strong>SDA</strong> — Static Data Authentication</td><td>✅</td><td>❌</td><td>b7 = 1</td></tr>
        <tr><td><strong>DDA</strong> — Dynamic Data Authentication</td><td>✅</td><td>✅</td><td>b6 = 1</td></tr>
        <tr><td><strong>CDA</strong> — Combined DDA / Generate AC</td><td>✅</td><td>✅ (+ bind với AC)</td><td>b1 = 1</td></tr>
    </table>
</div>

<div class="section">
    <h2>🔹 SDA — Static Data Authentication</h2>
    <p>Issuer tính một chữ ký RSA <em>một lần</em> trên dữ liệu tĩnh (PAN, expiry, AIP…) khi cá nhân hóa thẻ. Chữ ký này lưu trong tag <code>93</code> (Signed Static Application Data).</p>

    <h3>Flow SDA</h3>
    <div class="flow-step"><div class="step-number">1</div><div class="step-content"><h4>Lấy CA Public Key</h4><p>Đọc CA Public Key Index (<code>8F</code>) → tra trong bảng CA cài sẵn → lấy CA PK + exponent.</p></div></div>
    <div class="flow-step"><div class="step-number">2</div><div class="step-content"><h4>Recover Issuer PK</h4><p>Đọc Issuer PK Certificate (<code>90</code>), Issuer PK Remainder (<code>92</code>), Issuer PK Exponent (<code>9F32</code>). RSA recover bằng CA PK → có Issuer PK đầy đủ. Verify hash, expiry, PAN range.</p></div></div>
    <div class="flow-step"><div class="step-number">3</div><div class="step-content"><h4>Verify SDAD</h4><p>Đọc Signed Static Application Data (<code>93</code>). RSA recover bằng Issuer PK. So sánh hash bên trong với hash(static data đọc từ card + AIP). Nếu khớp → SDA pass.</p></div></div>

    <div class="danger-box">
        <h3>🚨 Vì sao SDA dễ bị clone?</h3>
        <p>Chữ ký <code>93</code> là <em>tĩnh</em> — kẻ tấn công đọc một lần là copy toàn bộ. Sau đó nạp lên một "yes-card" (thẻ giả luôn trả PIN OK offline) là dùng được offline. EMVCo khuyến cáo dừng phát hành SDA-only từ 2015.</p>
    </div>
</div>

<div class="section">
    <h2>🔸 DDA — Dynamic Data Authentication</h2>
    <p>Card có <strong>private key riêng</strong> (ICC private key) trong secure element. Mỗi giao dịch, terminal challenge bằng số ngẫu nhiên — card phải ký bằng private key — terminal verify bằng ICC public key.</p>

    <h3>Flow DDA</h3>
    <div class="flow-step"><div class="step-number">1</div><div class="step-content"><h4>Verify chuỗi chứng chỉ (giống SDA bước 1-2)</h4><p>Recover Issuer PK → recover ICC PK Certificate (<code>9F46</code>), ICC PK Remainder (<code>9F48</code>), ICC PK Exponent (<code>9F47</code>) bằng Issuer PK.</p></div></div>
    <div class="flow-step"><div class="step-number">2</div><div class="step-content"><h4>Build DDOL data</h4><p>Đọc DDOL (tag <code>9F49</code>) từ card. Nếu không có, dùng "Default DDOL" = tag <code>9F37</code> 4 byte (UN).</p></div></div>
    <div class="flow-step"><div class="step-number">3</div><div class="step-content"><h4>INTERNAL AUTHENTICATE</h4>
    <div class="code-block">&gt;&gt; <span class="hex">00 88 00 00 04 [UN 4 byte] 00</span>

&lt;&lt; <span class="hex">77 81 83
     9F 4B 81 80 [Signed Dynamic Application Data: 128 byte]
   90 00</span></div>
    </div></div>
    <div class="flow-step"><div class="step-number">4</div><div class="step-content"><h4>Verify SDAD</h4><p>RSA recover bằng ICC PK. Bên trong chứa: header, ICC Dynamic Data (gồm ICC Dynamic Number, optional Cryptogram Information Data...), hash của (recovered data || DDOL data || UN), trailer. So sánh hash → DDA pass.</p></div></div>

    <p>Vì challenge <strong>khác nhau mỗi giao dịch</strong>, kẻ tấn công có nghe trộm cũng không tái dùng được. Để clone thẻ DDA, cần lấy được ICC private key — không xảy ra trên chip đạt EAL4+.</p>
</div>

<div class="section">
    <h2>🔷 CDA — Combined DDA / Application Cryptogram Generation</h2>
    <p>SDA và DDA chỉ verify <em>tính xác thực card</em>, không bảo vệ riêng cryptogram. Nếu kênh giữa terminal và card bị MITM, attacker có thể đổi cryptogram. CDA giải quyết bằng cách <strong>gộp DDA vào GENERATE AC</strong>:</p>

    <ol>
        <li>Terminal gọi GENERATE AC với <code>P1 = 0x50</code> (TC + CDA) hoặc <code>0x90</code> (ARQC + CDA).</li>
        <li>Card ký <em>cùng lúc</em> ICC Dynamic Data + AC + ATC + IAD + hash của các giá trị giao dịch bằng ICC private key.</li>
        <li>Terminal verify chữ ký này — nghĩa là verify cả "card thật" và "cryptogram không bị đổi".</li>
    </ol>

    <div class="info-box">
        <h3>✅ CDA là mặc định ngày nay</h3>
        <p>Hầu hết thẻ mới (đặc biệt là Mastercard M/Chip Advance và Visa VSDC) đều bật CDA. Bit AIP b1 = 1 báo card hỗ trợ CDA.</p>
    </div>
</div>

<div class="section">
    <h2>📋 Tag liên quan ODA — bảng tra nhanh</h2>
    <table>
        <tr><th>Tag</th><th>Tên</th><th>Vai trò</th></tr>
        <tr><td><code>8F</code></td><td>CA Public Key Index</td><td>Trỏ tới CA key trong bảng terminal</td></tr>
        <tr><td><code>90</code></td><td>Issuer Public Key Certificate</td><td>RSA-signed bởi CA, chứa Issuer PK</td></tr>
        <tr><td><code>92</code></td><td>Issuer Public Key Remainder</td><td>Bit còn lại của Issuer PK (nếu certificate không chứa hết)</td></tr>
        <tr><td><code>9F32</code></td><td>Issuer Public Key Exponent</td><td>Thường là 03 hoặc 010001</td></tr>
        <tr><td><code>93</code></td><td>Signed Static Application Data (SDAD)</td><td>Dùng cho SDA</td></tr>
        <tr><td><code>9F46</code></td><td>ICC Public Key Certificate</td><td>RSA-signed bởi Issuer, chứa ICC PK</td></tr>
        <tr><td><code>9F47</code></td><td>ICC Public Key Exponent</td><td></td></tr>
        <tr><td><code>9F48</code></td><td>ICC Public Key Remainder</td><td></td></tr>
        <tr><td><code>9F49</code></td><td>DDOL</td><td>Danh sách tag cho INTERNAL AUTHENTICATE</td></tr>
        <tr><td><code>9F4A</code></td><td>Static Data Authentication Tag List</td><td>Liệt kê tag phải đưa vào hash khi tính SDAD/SDA</td></tr>
        <tr><td><code>9F4B</code></td><td>Signed Dynamic Application Data (SDAD)</td><td>Dùng cho DDA/CDA</td></tr>
    </table>
</div>

<div class="section">
    <h2>🛡️ Tóm tắt cơ chế chống fraud</h2>
    <table>
        <tr><th>Tấn công</th><th>SDA</th><th>DDA</th><th>CDA</th></tr>
        <tr><td>Đổi PAN/expiry trên chip</td><td>❌ Phát hiện</td><td>❌ Phát hiện</td><td>❌ Phát hiện</td></tr>
        <tr><td>Clone card (yes-card)</td><td>⚠️ Bị clone được</td><td>❌ Bị chặn</td><td>❌ Bị chặn</td></tr>
        <tr><td>MITM đổi cryptogram</td><td>—</td><td>⚠️ Có thể</td><td>❌ Bị chặn</td></tr>
        <tr><td>Replay cryptogram cũ</td><td>—</td><td>❌ ATC chống</td><td>❌ ATC chống</td></tr>
    </table>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>ODA</dt><dd>Offline Data Authentication — tổng tên cho SDA/DDA/CDA.</dd>
        <dt>SDA</dt><dd>Static Data Authentication — chữ ký RSA tĩnh trên dữ liệu thẻ.</dd>
        <dt>DDA</dt><dd>Dynamic Data Authentication — card ký challenge UN bằng ICC private key.</dd>
        <dt>CDA</dt><dd>Combined DDA / Application Cryptogram — kết hợp DDA vào GENERATE AC.</dd>
        <dt>SDAD</dt><dd>Signed Dynamic Application Data — tag <code>9F4B</code>, output của DDA/CDA.</dd>
        <dt>Certificate chain</dt><dd>CA → Issuer (tag 90) → ICC (tag 9F46).</dd>
        <dt>Yes-card</dt><dd>Thẻ giả luôn nói "PIN OK" — đe doạ chính của SDA-only.</dd>
        <dt>Default DDOL</dt><dd>Nếu thẻ không cung cấp DDOL, terminal dùng "9F37 04" (chỉ UN) — định nghĩa trong EMV Book 3.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>AIP của thẻ = <code>5C 00</code>. Bit b1 byte 1 = 0, b3 = 1, b4 = 1, b6 = 1, b7 = 1 → thẻ hỗ trợ những gì?</li>
        <li>Vì sao kẻ tấn công không thể clone thẻ DDA?</li>
        <li>Khi nào terminal dùng Default DDOL?</li>
        <li>Liệt kê 5 tag tối thiểu cần đọc trước khi thực hiện DDA.</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>ODA gồm 3 cấp: SDA (chữ ký tĩnh, dễ clone), DDA (challenge-response), CDA (DDA + AC).</li>
        <li>Terminal phải verify chuỗi: CA → Issuer Cert (90) → ICC Cert (9F46).</li>
        <li>SDA chỉ verify dữ liệu không bị đổi; DDA + CDA mới chống clone.</li>
        <li>EMVCo khuyến cáo CDA cho mọi thẻ mới (AIP bit b1 byte 1).</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 8: Android NFC + EMV
# ============================================================
LESSON_08 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu kiến trúc NFC trên Android (NfcAdapter, Tag, IsoDep).</li>
        <li>Setup permission và intent filter đúng cho payment card.</li>
        <li>Viết được hàm gửi APDU bằng Kotlin và xử lý SW.</li>
        <li>Hiểu Foreground Dispatch và Reader Mode (API 19+).</li>
    </ul>
</div>

<div class="section">
    <h2>📦 Android NFC stack</h2>
    <div class="diagram"><pre>
                    Your App (Kotlin)
                          │
                          ▼
              android.nfc.tech.IsoDep        (ISO 14443-4 wrapper, gửi APDU)
                          │
                          ▼
              android.nfc.Tag                (tag handle do hệ thống cấp)
                          │
                          ▼
              android.nfc.NfcAdapter         (entry point của NFC stack)
                          │
                          ▼
              NFC Service (system)           (giao tiếp với NFC controller chip)
                          │
                          ▼
              ┌───────────────────────┐
              │  Reader/Writer mode   │       Đọc thẻ ⟵ chúng ta dùng cái này
              │  HCE                  │       Phone đóng vai thẻ
              │  Peer-to-peer (legacy)│
              └───────────────────────┘
    </pre></div>

    <p><strong>IsoDep</strong> là class cao cấp nhất chúng ta cần: nó cung cấp <code>transceive(byte[])</code> gửi C-APDU và trả về R-APDU.</p>
</div>

<div class="section">
    <h2>🔧 AndroidManifest.xml</h2>
    <div class="code-block">&lt;manifest xmlns:android="http://schemas.android.com/apk/res/android"&gt;
    <span class="comment">&lt;!-- Permission --&gt;</span>
    &lt;uses-permission android:name="android.permission.NFC" /&gt;

    <span class="comment">&lt;!-- Yêu cầu thiết bị có NFC để hiện trên Play Store --&gt;</span>
    &lt;uses-feature android:name="android.hardware.nfc" android:required="true" /&gt;

    &lt;application&gt;
        &lt;activity android:name=".ReadCardActivity" android:launchMode="singleTop"&gt;
            <span class="comment">&lt;!-- Filter intent khi user chạm thẻ contactless --&gt;</span>
            &lt;intent-filter&gt;
                &lt;action android:name="android.nfc.action.TECH_DISCOVERED" /&gt;
            &lt;/intent-filter&gt;
            &lt;meta-data
                android:name="android.nfc.action.TECH_DISCOVERED"
                android:resource="@xml/nfc_tech_filter" /&gt;
        &lt;/activity&gt;
    &lt;/application&gt;
&lt;/manifest&gt;</div>

    <h3>res/xml/nfc_tech_filter.xml</h3>
    <div class="code-block">&lt;resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2"&gt;
    &lt;tech-list&gt;
        &lt;tech&gt;android.nfc.tech.IsoDep&lt;/tech&gt;
        &lt;tech&gt;android.nfc.tech.NfcA&lt;/tech&gt;
    &lt;/tech-list&gt;
    &lt;tech-list&gt;
        &lt;tech&gt;android.nfc.tech.IsoDep&lt;/tech&gt;
        &lt;tech&gt;android.nfc.tech.NfcB&lt;/tech&gt;
    &lt;/tech-list&gt;
&lt;/resources&gt;</div>

    <div class="info-box">
        <h3>💡 Vì sao 2 tech-list?</h3>
        <p>EMV contactless dùng cả ISO 14443 Type A (Visa, JCB…) và Type B (Amex, một số JCB). Phải khai báo riêng để intent fire cho cả 2 loại.</p>
    </div>
</div>

<div class="section">
    <h2>📡 Reader Mode (khuyến nghị cho EMV)</h2>
    <p>Từ API 19, Android có <code>enableReaderMode()</code> — cho phép disable các tính năng làm gián đoạn (như "Android Beam") và chỉ bật một subset tech. Đây là cách <strong>chính thức</strong> mọi POS Android dùng:</p>

    <div class="code-block">class ReadCardActivity : AppCompatActivity(), NfcAdapter.ReaderCallback {

    private lateinit var nfcAdapter: NfcAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_read)
        nfcAdapter = NfcAdapter.getDefaultAdapter(this)
            ?: throw IllegalStateException("Device không có NFC")
    }

    override fun onResume() {
        super.onResume()
        val options = Bundle().apply {
            <span class="comment">// timeout transceive (ms)</span>
            putInt(NfcAdapter.EXTRA_READER_PRESENCE_CHECK_DELAY, 250)
        }
        nfcAdapter.enableReaderMode(
            this,
            this,
            NfcAdapter.FLAG_READER_NFC_A
                or NfcAdapter.FLAG_READER_NFC_B
                or NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK,
            options
        )
    }

    override fun onPause() {
        super.onPause()
        nfcAdapter.disableReaderMode(this)
    }

    override fun onTagDiscovered(tag: Tag) {
        val isoDep = IsoDep.get(tag) ?: return    <span class="comment">// thẻ không hỗ trợ 14443-4</span>
        try {
            isoDep.connect()
            isoDep.timeout = 5_000                 <span class="comment">// 5s cho từng APDU</span>
            readEmv(isoDep)
        } finally {
            try { isoDep.close() } catch (_: Exception) {}
        }
    }
}</div>
</div>

<div class="section">
    <h2>📤 Gửi APDU</h2>
    <div class="code-block">private fun readEmv(isoDep: IsoDep) {
    <span class="comment">// 1) SELECT PPSE</span>
    val ppseResp = isoDep.transceive(buildSelectPpse())
    val ppseR = ResponseApdu.parse(ppseResp)
    require(ppseR.isSuccess) { "SELECT PPSE failed: SW=${ppseR.swHex()}" }

    val ppseTlv = TlvParser(ppseR.data).parseAll()
    val aid = ppseTlv.findTag(0x4F)?.value
        ?: error("No AID in PPSE response")

    <span class="comment">// 2) SELECT AID</span>
    val selectAid = CommandApdu(0x00, 0xA4.toByte(), 0x04, 0x00, aid, 0x00).toBytes()
    val aidR = ResponseApdu.parse(isoDep.transceive(selectAid))
    require(aidR.isSuccess) { "SELECT AID failed: SW=${aidR.swHex()}" }

    val aidTlv = TlvParser(aidR.data).parseAll()
    val pdolTemplate = aidTlv.findTag(0x9F38)?.value   <span class="comment">// có thể null</span>

    <span class="comment">// 3) Build GPO data</span>
    val pdolData = buildPdolData(pdolTemplate)
    val gpoData = byteArrayOf(0x83.toByte(), pdolData.size.toByte()) + pdolData
    val gpo = CommandApdu(0x80.toByte(), 0xA8.toByte(), 0x00, 0x00, gpoData, 0x00).toBytes()
    val gpoR = ResponseApdu.parse(isoDep.transceive(gpo))
    require(gpoR.isSuccess) { "GPO failed: SW=${gpoR.swHex()}" }

    <span class="comment">// 4) Parse AFL và READ RECORD</span>
    val gpoTlv = TlvParser(gpoR.data).parseAll()
    val afl = gpoTlv.findTag(0x94)?.value
        ?: gpoR.data.copyOfRange(2 + (gpoR.data[1].toInt() and 0xFF), gpoR.data.size)  <span class="comment">// format 1: 80 lenAIP AIP AFL</span>

    val records = mutableListOf&lt;Tlv&gt;()
    afl.asList().chunked(4).forEach { (b0, b1, b2, _) ->
        val sfi = (b0.toInt() and 0xFF) shr 3
        val first = b1.toInt() and 0xFF
        val last = b2.toInt() and 0xFF
        for (rec in first..last) {
            val rd = ResponseApdu.parse(
                isoDep.transceive(CommandApdu(0x00, 0xB2, rec.toByte(), ((sfi shl 3) or 0x04).toByte(), null, 0x00).toBytes())
            )
            if (rd.isSuccess) records += TlvParser(rd.data).parseAll()
        }
    }

    <span class="comment">// 5) Lấy PAN, expiry, name…</span>
    val pan = records.findTag(0x5A)?.value?.toHex()
    val expiry = records.findTag(0x5F24)?.value?.toHex()
    val name = records.findTag(0x5F20)?.let { String(it.value, Charsets.US_ASCII).trim() }

    runOnUiThread { showCardInfo(maskPan(pan), expiry, name) }
}

private fun buildSelectPpse() = CommandApdu(
    0x00, 0xA4.toByte(), 0x04, 0x00,
    "2PAY.SYS.DDF01".toByteArray(Charsets.US_ASCII),
    0x00
).toBytes()</div>
</div>

<div class="section">
    <h2>🧮 Build PDOL data (helper)</h2>
    <div class="code-block">private fun buildPdolData(pdolTemplate: ByteArray?): ByteArray {
    if (pdolTemplate == null || pdolTemplate.isEmpty()) return byteArrayOf()

    val out = mutableListOf&lt;Byte&gt;()
    var i = 0
    while (i &lt; pdolTemplate.size) {
        <span class="comment">// đọc tag</span>
        val tagStart = i
        var tag = pdolTemplate[i++].toInt() and 0xFF
        if ((tag and 0x1F) == 0x1F) {
            tag = (tag shl 8) or (pdolTemplate[i++].toInt() and 0xFF)
        }
        val len = pdolTemplate[i++].toInt() and 0xFF

        val value: ByteArray = when (tag) {
            0x9F66 -&gt; byteArrayOf(0x36, 0x00, 0x40, 0x80)                <span class="comment">// TTQ: VSDC, online PIN ok</span>
            0x9F02 -&gt; "000000010000".hexToBytes()                          <span class="comment">// 1000.00 đơn vị</span>
            0x9F03 -&gt; ByteArray(6)
            0x9F1A -&gt; "0704".hexToBytes()                                  <span class="comment">// VN</span>
            0x95   -&gt; ByteArray(5)                                         <span class="comment">// TVR</span>
            0x5F2A -&gt; "0704".hexToBytes()                                  <span class="comment">// VND</span>
            0x9A   -&gt; nowAsYYMMDD()
            0x9C   -&gt; byteArrayOf(0x00)
            0x9F37 -&gt; SecureRandom().run { ByteArray(4).also(::nextBytes) }
            else   -&gt; ByteArray(len)
        }
        require(value.size == len) { "Wrong length for tag ${tag.toString(16)}" }
        out += value.toList()
    }
    return out.toByteArray()
}</div>
</div>

<div class="section">
    <h2>🛡️ Bảo mật và compliance ở phía client</h2>
    <ul>
        <li><strong>Không log PAN đầy đủ.</strong> Mask: <code>4532 •••• •••• 9010</code>. Vi phạm là vi phạm PCI DSS.</li>
        <li><strong>Không lưu PAN, CVV, PIN.</strong> Tuyệt đối. Nếu cần token, dùng tokenization service của ngân hàng.</li>
        <li><strong>Không dùng <code>SharedPreferences</code> cho dữ liệu thẻ.</strong> Bộ nhớ này có thể bị backup ra Google Drive.</li>
        <li><strong>Disable screenshot</strong> ở Activity hiển thị card data: <code>window.setFlags(FLAG_SECURE, FLAG_SECURE)</code>.</li>
        <li><strong>Foreground only.</strong> Đọc thẻ chỉ khi Activity đang resume — không bao giờ trong background service.</li>
    </ul>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>NfcAdapter</dt><dd>Entry-point API của Android NFC. <code>getDefaultAdapter(context)</code>.</dd>
        <dt>IsoDep</dt><dd>Class bọc ISO 14443-4: hàm chính là <code>transceive(byte[]): byte[]</code>.</dd>
        <dt>Reader Mode</dt><dd>API 19+ (<code>enableReaderMode</code>), tắt Android Beam/NDEF, ổn định nhất cho EMV.</dd>
        <dt>Foreground Dispatch</dt><dd>API cũ hơn (API 10+) để ưu tiên Activity nhận tag — vẫn dùng được nhưng không ổn định bằng Reader Mode.</dd>
        <dt>HCE</dt><dd>Host Card Emulation — Android app đóng vai thẻ (phần POS đọc app).</dd>
        <dt>FLAG_SECURE</dt><dd>Window flag chặn screenshot/screen recording — bắt buộc với UI hiển thị data thẻ.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Tạo project Android mới, copy <code>CommandApdu</code>/<code>ResponseApdu</code>/<code>TlvParser</code> từ bài 4-5 vào.</li>
        <li>Test thử SELECT PPSE với thẻ của bạn, in ra response hex.</li>
        <li>Bật <code>FLAG_SECURE</code> cho Activity và verify rằng screenshot bị chặn.</li>
        <li>Đo timeout: với thẻ chậm (như thẻ chip cũ), giá trị nào phù hợp?</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>Cần permission <code>android.permission.NFC</code> + uses-feature.</li>
        <li>Reader Mode (API 19+) là cách khuyến nghị, không bị NDEF/Android Beam can thiệp.</li>
        <li>IsoDep.transceive(byte[]) là API duy nhất bạn cần để gửi APDU.</li>
        <li>Bắt buộc: không log/lưu PAN/CVV/PIN; bật FLAG_SECURE; chỉ đọc khi Activity foreground.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 9: Demo đọc thẻ thật
# ============================================================
LESSON_09 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Ghép tất cả bài trước thành một demo Android hoàn chỉnh.</li>
        <li>Đọc và hiển thị: PAN (đã mask), expiry, cardholder name, AID, application label.</li>
        <li>Biết troubleshoot các lỗi phổ biến: 6A 82, 6A 83, 67 00.</li>
    </ul>
</div>

<div class="section">
    <h2>📂 Cấu trúc project</h2>
    <div class="code-block">app/
 └─ src/main/
     ├─ AndroidManifest.xml
     ├─ res/xml/nfc_tech_filter.xml
     ├─ res/layout/activity_main.xml
     └─ java/com/example/emvreader/
         ├─ MainActivity.kt
         ├─ apdu/
         │   ├─ CommandApdu.kt
         │   ├─ ResponseApdu.kt
         │   └─ Hex.kt
         ├─ tlv/
         │   ├─ Tlv.kt
         │   └─ TlvParser.kt
         └─ emv/
             ├─ EmvReader.kt
             └─ Pdol.kt</div>
</div>

<div class="section">
    <h2>📜 MainActivity.kt</h2>
    <div class="code-block">class MainActivity : AppCompatActivity(), NfcAdapter.ReaderCallback {

    private lateinit var nfcAdapter: NfcAdapter
    private lateinit var status: TextView
    private lateinit var details: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        window.setFlags(WindowManager.LayoutParams.FLAG_SECURE,
                        WindowManager.LayoutParams.FLAG_SECURE)
        status = findViewById(R.id.status)
        details = findViewById(R.id.details)
        nfcAdapter = NfcAdapter.getDefaultAdapter(this)
            ?: run {
                status.text = "Thiết bị không có NFC"
                return
            }
    }

    override fun onResume() {
        super.onResume()
        if (!nfcAdapter.isEnabled) {
            status.text = "NFC đang tắt — vào Settings để bật"
            return
        }
        status.text = "Đặt thẻ lên mặt sau điện thoại…"
        nfcAdapter.enableReaderMode(
            this, this,
            NfcAdapter.FLAG_READER_NFC_A or
            NfcAdapter.FLAG_READER_NFC_B or
            NfcAdapter.FLAG_READER_SKIP_NDEF_CHECK,
            null
        )
    }

    override fun onPause() {
        super.onPause()
        nfcAdapter.disableReaderMode(this)
    }

    override fun onTagDiscovered(tag: Tag) {
        val isoDep = IsoDep.get(tag) ?: return
        try {
            isoDep.connect()
            isoDep.timeout = 5_000
            val info = EmvReader(isoDep).read()
            runOnUiThread {
                status.text = "✅ Đọc thành công"
                details.text = info.prettyPrint()
            }
        } catch (e: Exception) {
            runOnUiThread {
                status.text = "❌ Lỗi"
                details.text = e.message ?: "Unknown"
            }
        } finally {
            try { isoDep.close() } catch (_: Exception) {}
        }
    }
}</div>
</div>

<div class="section">
    <h2>📜 EmvReader.kt — core flow</h2>
    <div class="code-block">data class CardInfo(
    val aid: String?,
    val applicationLabel: String?,
    val pan: String?,
    val expiry: String?,
    val cardholderName: String?,
    val track2: String?
) {
    fun prettyPrint() = buildString {
        appendLine("AID:             $aid")
        appendLine("App Label:       $applicationLabel")
        appendLine("PAN (masked):    ${pan?.let(::maskPan)}")
        appendLine("Expiry:          ${expiry?.let(::formatExpiry)}")
        appendLine("Cardholder:      $cardholderName")
        appendLine("Track 2:         ${track2?.let(::maskTrack2)}")
    }
}

class EmvReader(private val iso: IsoDep) {

    fun read(): CardInfo {
        val aidBytes = selectPpseAndPickAid()
        val fci = selectAid(aidBytes)
        val pdolTpl = fci.findTag(0x9F38)?.value
        val gpoTlv = getProcessingOptions(pdolTpl)
        val afl = extractAfl(gpoTlv)
        val records = readAllRecords(afl)

        val appLabel = fci.findTag(0x50)?.value?.let { String(it, Charsets.US_ASCII).trim() }
        val pan = records.findTag(0x5A)?.value?.toHex()?.trimEnd('F', 'f')
        val expiry = records.findTag(0x5F24)?.value?.toHex()
        val name = records.findTag(0x5F20)?.value?.let { String(it, Charsets.US_ASCII).trim() }
        val track2 = records.findTag(0x57)?.value?.toHex()

        return CardInfo(
            aid = aidBytes.toHex(),
            applicationLabel = appLabel,
            pan = pan,
            expiry = expiry,
            cardholderName = name,
            track2 = track2
        )
    }

    private fun selectPpseAndPickAid(): ByteArray {
        val ppseName = "2PAY.SYS.DDF01".toByteArray(Charsets.US_ASCII)
        val resp = transceive(CommandApdu(0x00, 0xA4.toByte(), 0x04, 0x00, ppseName, 0x00).toBytes())
        ensure(resp.isSuccess) { "SELECT PPSE → ${resp.swHex()}" }

        val tlv = TlvParser(resp.data).parseAll()
        return tlv.findTag(0x4F)?.value
            ?: throw IllegalStateException("Không thấy AID trong PPSE response")
    }

    private fun selectAid(aid: ByteArray): List&lt;Tlv&gt; {
        val resp = transceive(
            CommandApdu(0x00, 0xA4.toByte(), 0x04, 0x00, aid, 0x00).toBytes()
        )
        ensure(resp.isSuccess) { "SELECT AID → ${resp.swHex()}" }
        return TlvParser(resp.data).parseAll()
    }

    private fun getProcessingOptions(pdolTpl: ByteArray?): List&lt;Tlv&gt; {
        val pdolData = Pdol.build(pdolTpl)
        val dataField = byteArrayOf(0x83.toByte(), pdolData.size.toByte()) + pdolData
        val resp = transceive(
            CommandApdu(0x80.toByte(), 0xA8.toByte(), 0x00, 0x00, dataField, 0x00).toBytes()
        )
        ensure(resp.isSuccess) { "GPO → ${resp.swHex()}" }
        return TlvParser(resp.data).parseAll()
    }

    private fun extractAfl(gpoTlv: List&lt;Tlv&gt;): ByteArray {
        gpoTlv.findTag(0x94)?.let { return it.value }
        <span class="comment">// format 1 (80): byte[0..1] = AIP, byte[2..] = AFL</span>
        val format1 = gpoTlv.firstOrNull { it.tag == 0x80 }?.value
            ?: throw IllegalStateException("GPO không có AFL")
        return format1.copyOfRange(2, format1.size)
    }

    private fun readAllRecords(afl: ByteArray): List&lt;Tlv&gt; {
        val out = mutableListOf&lt;Tlv&gt;()
        var i = 0
        while (i &lt; afl.size) {
            val sfi = (afl[i].toInt() and 0xFF) shr 3
            val first = afl[i + 1].toInt() and 0xFF
            val last = afl[i + 2].toInt() and 0xFF
            i += 4
            for (rec in first..last) {
                val resp = transceive(
                    CommandApdu(0x00, 0xB2, rec.toByte(),
                                ((sfi shl 3) or 0x04).toByte(), null, 0x00).toBytes()
                )
                if (resp.isSuccess) out += TlvParser(resp.data).parseAll()
            }
        }
        return out
    }

    private fun transceive(cmd: ByteArray): ResponseApdu {
        val raw = iso.transceive(cmd)
        return ResponseApdu.parse(raw)
    }

    private inline fun ensure(cond: Boolean, msg: () -&gt; String) {
        if (!cond) throw IllegalStateException(msg())
    }
}

fun maskPan(pan: String) = pan.take(4) + " •••• •••• " + pan.takeLast(4)
fun formatExpiry(yymmdd: String) = "${yymmdd.substring(2,4)}/${yymmdd.substring(0,2)}"
fun maskTrack2(t2: String): String {
    val sep = t2.indexOf('D').takeIf { it &gt; 0 } ?: t2.indexOf('d')
    if (sep &lt; 0) return "(unparseable)"
    val pan = t2.substring(0, sep)
    return maskPan(pan) + "D" + t2.substring(sep + 1).take(4).padEnd(4, '*')
}</div>
</div>

<div class="section">
    <h2>🧪 Demo output (thẻ Vietcombank Visa Debit thật, đã ẩn số)</h2>
    <div class="code-block">AID:             A0000000031010
App Label:       VISA DEBIT
PAN (masked):    4532 •••• •••• 9010
Expiry:          12/27
Cardholder:      NGUYEN/VAN A
Track 2:         4532 •••• •••• 9010D2712****</div>
</div>

<div class="section">
    <h2>🐛 Troubleshooting</h2>
    <table>
        <tr><th>Triệu chứng</th><th>Nguyên nhân</th><th>Khắc phục</th></tr>
        <tr><td>Tag bị mất ngay sau khi connect</td><td>Thẻ rời antenna giữa các APDU</td><td>Tăng <code>EXTRA_READER_PRESENCE_CHECK_DELAY</code>, yêu cầu user giữ thẻ ổn định</td></tr>
        <tr><td>SELECT PPSE → <code>6A 82</code></td><td>Thẻ chip-only (không hỗ trợ contactless) hoặc thẻ Mifare Classic (không phải EMV)</td><td>Thẻ không có 2PAY.SYS.DDF01 — không phải EMV contactless</td></tr>
        <tr><td>READ RECORD → <code>6A 83</code></td><td>Record không tồn tại</td><td>Kiểm tra lại parse AFL — có thể bị off-by-one</td></tr>
        <tr><td>GPO → <code>67 00</code></td><td>Sai length của PDOL data</td><td>Verify mỗi field có đúng length spec yêu cầu</td></tr>
        <tr><td>Đọc Mastercard ra thấy AFL khác mỗi lần</td><td>Card random hóa AFL để chống fingerprinting</td><td>Bình thường — luôn parse AFL từ response, không hardcode</td></tr>
        <tr><td><code>java.io.IOException: Transceive failed</code></td><td>Thẻ rời quá sớm hoặc APDU malformed</td><td>Wrap retry 1-2 lần, kiểm tra log APDU hex</td></tr>
    </table>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Implement project trên Android Studio. Test với thẻ Visa, Mastercard, JCB của bạn.</li>
        <li>Thêm hiển thị Track 2 expiry và service code (parse riêng nibble từ Track 2 equivalent).</li>
        <li>Khi card có nhiều AID, hiện UI cho user chọn thay vì lấy AID đầu tiên.</li>
        <li>Thêm chống đọc lặp lại quá nhanh (debounce 1s sau khi đọc thành công).</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>EmvReader thực hiện đúng 4 bước: SELECT PPSE → SELECT AID → GPO → READ RECORD.</li>
        <li>Mask PAN khi hiển thị; bật FLAG_SECURE; không lưu/log dữ liệu nhạy cảm.</li>
        <li>Luôn parse AFL từ response — đừng hardcode SFI.</li>
        <li>Hiểu SW phổ biến để debug nhanh.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 10: Bảo mật & PCI DSS
# ============================================================
LESSON_10 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu PCI DSS là gì và áp dụng cho ai.</li>
        <li>Phân biệt 3 nhóm dữ liệu: PAN, SAD, và dữ liệu được phép lưu.</li>
        <li>Biết khái niệm tokenization và P2PE.</li>
        <li>Áp dụng best practice bảo mật cho Android app đọc thẻ.</li>
    </ul>
</div>

<div class="section">
    <h2>📜 PCI DSS là gì?</h2>
    <p><strong>PCI DSS</strong> (Payment Card Industry Data Security Standard) là chuẩn bảo mật do <strong>PCI Security Standards Council</strong> (PCI SSC) duy trì — tổ chức do Amex, Discover, JCB, Mastercard, Visa sáng lập 2006. Phiên bản hiện hành là <strong>PCI DSS v4.0.1</strong> (06/2024).</p>

    <p>Chuẩn quy định <strong>12 yêu cầu</strong>, chia thành 6 nhóm:</p>
    <table>
        <tr><th>Nhóm</th><th>Yêu cầu</th></tr>
        <tr><td>Build &amp; Maintain Secure Network</td><td>1. Firewall &nbsp;·&nbsp; 2. Không dùng vendor default</td></tr>
        <tr><td>Protect Cardholder Data</td><td>3. Bảo vệ stored CHD &nbsp;·&nbsp; 4. Mã hóa khi truyền</td></tr>
        <tr><td>Vulnerability Management</td><td>5. Anti-malware &nbsp;·&nbsp; 6. Secure dev practices</td></tr>
        <tr><td>Strong Access Control</td><td>7. Least privilege &nbsp;·&nbsp; 8. Unique ID &nbsp;·&nbsp; 9. Physical access</td></tr>
        <tr><td>Monitor &amp; Test Networks</td><td>10. Log all access &nbsp;·&nbsp; 11. Pen-test định kỳ</td></tr>
        <tr><td>Information Security Policy</td><td>12. Policy chính thức</td></tr>
    </table>

    <div class="info-box">
        <h3>👤 Ai phải tuân thủ?</h3>
        <p>Mọi tổ chức <strong>store / process / transmit cardholder data</strong>. Tùy số lượng giao dịch/năm, được chia level 1 đến 4 với mức độ audit khác nhau. Là Android dev đọc thẻ → bạn (hoặc công ty bạn) thuộc <em>scope</em> PCI DSS dù chỉ "lướt qua" PAN trong RAM.</p>
    </div>
</div>

<div class="section">
    <h2>📊 Dữ liệu — gì lưu được, gì không</h2>

    <h3>Cardholder Data (CHD)</h3>
    <table>
        <tr><th>Trường</th><th>Lưu được?</th><th>Bắt buộc mã hóa khi lưu</th></tr>
        <tr><td>PAN</td><td>✅ (nhưng phải mã hóa)</td><td>✅ Strong cryptography (AES-256, RSA-2048…)</td></tr>
        <tr><td>Cardholder Name</td><td>✅</td><td>Tuỳ chính sách</td></tr>
        <tr><td>Service Code</td><td>✅</td><td>Tuỳ</td></tr>
        <tr><td>Expiration Date</td><td>✅</td><td>Tuỳ</td></tr>
    </table>

    <h3>Sensitive Authentication Data (SAD) — TUYỆT ĐỐI KHÔNG LƯU SAU AUTH</h3>
    <table>
        <tr><th>Trường</th><th>Lưu được?</th></tr>
        <tr><td>Full Track 1 / Track 2 / equivalent chip data</td><td>❌</td></tr>
        <tr><td>CAV2 / CVC2 / CVV2 / CID (3-4 số sau thẻ)</td><td>❌</td></tr>
        <tr><td>PIN / PIN Block</td><td>❌</td></tr>
    </table>

    <div class="danger-box">
        <h3>🚨 Bao gồm cả "tạm" trong RAM</h3>
        <p>PCI DSS Requirement 3.3.1: SAD <em>không được lưu sau khi authorization hoàn tất</em>, kể cả encrypted. Trong Android: bạn có thể đọc Track 2 từ tag 57 để display, nhưng <strong>không được</strong> ghi vào file/preferences/database/log.</p>
    </div>

    <h3>PAN masking — Requirement 3.4</h3>
    <p>Khi hiển thị PAN: tối đa <strong>6 số đầu + 4 số cuối</strong> (BIN + last4). Lý tưởng là <em>chỉ last4</em>.</p>
    <div class="code-block">PAN gốc:    4532 1234 5678 9010
Hiển thị:   4532 12•• •••• 9010   ✅
Hiển thị:   •••• •••• •••• 9010   ✅ (better)
Hiển thị:   4532 1234 5678 9010   ❌ (full)</div>
</div>

<div class="section">
    <h2>🪙 Tokenization — đỡ phải đối mặt với PCI</h2>
    <p>Thay vì lưu PAN, gửi PAN cho <strong>Token Service Provider</strong> (TSP) → nhận lại <strong>token</strong> (cũng 16 số, có thể qua Luhn check) — token được lưu thay PAN.</p>

    <ul>
        <li>Visa: <strong>Visa Token Service (VTS)</strong></li>
        <li>Mastercard: <strong>MDES (Mastercard Digital Enablement Service)</strong></li>
        <li>Spec: <strong>EMV Payment Tokenisation Specification — Technical Framework v2.3</strong></li>
    </ul>

    <p>Token chỉ map ngược về PAN bên trong TSP. Token đi qua cả pipeline merchant/acquirer/network mà PAN thật không bao giờ rời TSP. Đây là cơ chế đằng sau Apple Pay, Google Pay, Samsung Pay.</p>

    <div class="info-box">
        <h3>💡 Token vs surrogate PAN trong merchant DB</h3>
        <p>Một số merchant lớn dùng "internal tokenization": tự sinh token nội bộ (UUID) thay PAN. Vẫn phải mã hóa map bảng theo PCI DSS Requirement 3.5/3.6, nhưng <em>scope</em> nhỏ hơn nhiều so với lưu PAN trực tiếp.</p>
    </div>
</div>

<div class="section">
    <h2>🔐 P2PE — Point-to-Point Encryption</h2>
    <p>Với POS chấp nhận thẻ, dữ liệu PAN được encrypt <em>ngay tại reader</em> bằng key của payment processor, đi end-to-end về backend processor mà merchant không bao giờ "thấy" plaintext PAN. Đây là validated solution của PCI SSC → giảm cực nhiều scope audit.</p>
</div>

<div class="section">
    <h2>📱 Best practices cho Android app đọc thẻ</h2>

    <div class="success-box">
        <h3>✅ DO</h3>
        <ul>
            <li>Dùng <code>ByteArray</code>/<code>CharArray</code> rồi <code>Arrays.fill(0)</code> sau khi xong. Tránh String (immutable, GC không xóa ngay).</li>
            <li>Disable backup: <code>android:allowBackup="false"</code> trong manifest.</li>
            <li><code>FLAG_SECURE</code> cho Activity hiển thị data.</li>
            <li>Yêu cầu Android 11+ (<code>minSdk = 30</code>): scoped storage, không có legacy external storage rủi ro.</li>
            <li>Verify SSL pinning khi gọi backend.</li>
            <li>Obfuscate (R8 / ProGuard) — ít nhất là kebab tên class crypto.</li>
            <li>Test trên thẻ thật + RFID-blocking sleeve để verify khoảng cách đọc.</li>
        </ul>
    </div>

    <div class="danger-box">
        <h3>❌ DON'T</h3>
        <ul>
            <li>KHÔNG lưu PAN/CVV/Track/PIN ở <code>SharedPreferences</code>, <code>Room</code>, file, log.</li>
            <li>KHÔNG ghi APDU response thô vào Logcat ở build release.</li>
            <li>KHÔNG gửi PAN qua HTTP plaintext — chỉ TLS 1.2+, ưu tiên TLS 1.3.</li>
            <li>KHÔNG dùng RSA-1024 / SHA-1 cho key mới sinh ở backend.</li>
            <li>KHÔNG chạy app trên thiết bị rooted/emulator ở môi trường production (sử dụng SafetyNet/Play Integrity).</li>
            <li>KHÔNG cố giải mã offline PIN — không thể, và là vi phạm pháp luật.</li>
        </ul>
    </div>
</div>

<div class="section">
    <h2>⚖️ Pháp lý ở Việt Nam</h2>
    <ul>
        <li><strong>Nghị định 13/2023/NĐ-CP</strong> (Bảo vệ dữ liệu cá nhân) — PAN, thông tin tài khoản thuộc dữ liệu cá nhân nhạy cảm.</li>
        <li><strong>Thông tư 47/2014/TT-NHNN</strong> và các thông tư sửa đổi — quy định an toàn bảo mật trong cung ứng dịch vụ thanh toán.</li>
        <li><strong>Luật An ninh mạng 2018</strong> — áp dụng cho mọi hệ thống xử lý thông tin thanh toán.</li>
    </ul>
    <p>Khi triển khai app production, làm việc cùng đội pháp chế là bắt buộc.</p>
</div>

<div class="section">
    <h2>📚 Tài liệu chính thức bạn nên đọc</h2>
    <ol>
        <li><strong>EMV Integrated Circuit Card Specifications for Payment Systems v4.4</strong> — emvco.com, free.</li>
        <li><strong>EMV Contactless Specifications</strong> (Book A, B, C-1..C-8) — emvco.com.</li>
        <li><strong>EMV Payment Tokenisation Specification — Technical Framework v2.3</strong>.</li>
        <li><strong>PCI DSS v4.0.1</strong> — pcisecuritystandards.org, free download.</li>
        <li><strong>ISO/IEC 7816-3, 7816-4, 7816-5</strong> — mua trên iso.org, hoặc đọc tóm tắt ở các vendor doc.</li>
        <li><strong>ISO/IEC 14443-1..4</strong> — chuẩn RF cho contactless.</li>
        <li><strong>ISO/IEC 9796-2</strong> — RSA signature scheme dùng trong EMV.</li>
        <li><strong>ISO/IEC 9797-1</strong> — MAC algorithm 3 dùng cho AC.</li>
    </ol>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>PCI DSS</dt><dd>Payment Card Industry Data Security Standard, v4.0.1 (2024), do PCI SSC duy trì.</dd>
        <dt>CHD</dt><dd>Cardholder Data — gồm PAN, Cardholder Name, Service Code, Expiration Date.</dd>
        <dt>SAD</dt><dd>Sensitive Authentication Data — Track data, CVV2/CVC2/CID, PIN/PIN Block. KHÔNG được lưu sau auth.</dd>
        <dt>Tokenization</dt><dd>Thay PAN bằng token (16 số) thông qua Token Service Provider (Visa VTS, Mastercard MDES).</dd>
        <dt>P2PE</dt><dd>Point-to-Point Encryption — encrypt PAN ngay từ reader đến backend processor.</dd>
        <dt>BIN</dt><dd>Bank Identification Number — 6 số đầu PAN (đang được mở rộng thành 8 số). Cho biết issuer.</dd>
        <dt>Scope</dt><dd>Tập các hệ thống nằm trong phạm vi PCI DSS audit.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập cuối khóa</h3>
    <ol>
        <li>Review code Android của bạn từ bài 8-9. Tìm và sửa: log PAN, lưu vào SharedPreferences, thiếu FLAG_SECURE.</li>
        <li>Đọc PCI DSS v4.0.1 Requirement 3 (download free). List 5 yêu cầu cụ thể áp dụng cho code Android của bạn.</li>
        <li>Demo tokenization "mini": app gửi PAN qua TLS đến backend → backend trả về token UUID → app chỉ lưu token.</li>
        <li>Viết security checklist 20 mục cho app payment Android, dùng cho mọi project sau này.</li>
    </ol>
</div>

<div class="success-box">
    <h3>🎓 Hoàn tất khóa học</h3>
    <p>Bạn đã đi qua:</p>
    <ul>
        <li>Khái niệm EMV, kiến trúc thẻ, file system.</li>
        <li>Toàn bộ transaction flow theo EMV Book 3.</li>
        <li>APDU theo ISO 7816-4, BER-TLV và mọi tag EMV phổ biến.</li>
        <li>Cryptography (RSA, 3DES/AES, SHA, MAC) và key hierarchy CA/Issuer/ICC.</li>
        <li>Offline Data Authentication: SDA / DDA / CDA.</li>
        <li>Code Android dùng NfcAdapter Reader Mode + IsoDep để đọc thẻ thật.</li>
        <li>PCI DSS, tokenization, P2PE và best practice bảo mật.</li>
    </ul>
    <p>Tiếp theo: đọc spec gốc EMVCo. Mọi thứ trong khóa học này đều bắt nguồn từ đó — và spec là <em>nguồn chân lý</em> duy nhất.</p>
</div>
'''

