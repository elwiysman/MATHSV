import sympy as sp
import uuid

def create_latex_steps(operation, expression, variables, params, result, intermediate_steps=None):
    """Create detailed LaTeX steps for mathematical operations"""
    steps = [] 
    
    try:
        if operation == 'pecahan': 
            action = params.get("action", "simplify") 
            expr1 = params.get("expr1", "1/2") 
            expr2 = params.get("expr2", "1/3") 
            
            frac1 = sp.Rational(expr1) 
            frac2 = sp.Rational(expr2) if expr2 else None 
            
            steps.append({ 
                'description': 'Operasi Pecahan',
                'latex': f'\\text{{Operasi: }} {action.replace("_", " ").title()}'
            })
            
            if action == "simplify": 
                steps.append({ 
                    'description': 'Pecahan Asli',
                    'latex': f'{sp.latex(frac1)}'
                })
                steps.append({ 
                    'description': 'Cari FPB pembilang dan penyebut',
                    'latex': f'\\text{{FPB dari }} {frac1.numerator} \\text{{ dan }} {frac1.denominator} = {sp.gcd(frac1.numerator, frac1.denominator)}'
                })
                steps.append({ 
                    'description': 'Sederhanakan pecahan dengan membagi pembilang dan penyebut dengan FPB',
                    'latex': f'\\frac{{{frac1.numerator} \\div {sp.gcd(frac1.numerator, frac1.denominator)}}}{{{frac1.denominator} \\div {sp.gcd(frac1.numerator, frac1.denominator)}}} = \\boxed{{{sp.latex(result)}}}'
                })
            elif action in ["add", "subtract"]: 
                operator = "+" if action == "add" else "-" 
                steps.append({ 
                    'description': 'Pecahan Asli',
                    'latex': f'{sp.latex(frac1)} {operator} {sp.latex(frac2)}'
                })
                
                denom1 = frac1.denominator 
                denom2 = frac2.denominator 
                lcm = sp.lcm(denom1, denom2) 
                
                steps.append({ 
                    'description': 'Cari penyebut umum (KPK)',
                    'latex': f'\\text{{KPK dari }} {denom1} \\text{{ dan }} {denom2} = {lcm}'
                })
                
                steps.append({ 
                    'description': 'Ubah pecahan ke penyebut umum',
                    'latex': f'\\frac{{{frac1.numerator} \\times {lcm // denom1}}}{{{lcm}}} {operator} \\frac{{{frac2.numerator} \\times {lcm // denom2}}}{{{lcm}}}'
                })
                
                steps.append({ 
                    'description': 'Lakukan operasi pada pembilang',
                    'latex': f'\\frac{{{frac1.numerator * (lcm // denom1)} {operator} {frac2.numerator * (lcm // denom2)}}}{{{lcm}}}'
                })
                
                combined_num = frac1.numerator * (lcm // denom1) + (frac2.numerator * (lcm // denom2) if action == "add" else -frac2.numerator * (lcm // denom2)) 
                steps.append({ 
                    'description': 'Gabungkan pembilang',
                    'latex': f'\\frac{{{combined_num}}}{{{lcm}}}'
                })
                
                if sp.gcd(combined_num, lcm) != 1: 
                    steps.append({ 
                        'description': 'Sederhanakan hasilnya',
                        'latex': f'\\frac{{{combined_num} \\div {sp.gcd(combined_num, lcm)}}}{{{lcm} \\div {sp.gcd(combined_num, lcm)}}} = \\boxed{{{sp.latex(result)}}}'
                    })
                else:
                    steps.append({ 
                        'description': 'Hasil akhir (sudah disederhanakan)',
                        'latex': f'\\boxed{{{sp.latex(result)}}}'
                    })
            elif action == "multiply": 
                operator = "\\times" 
                steps.append({ 
                    'description': 'Pecahan Asli',
                    'latex': f'{sp.latex(frac1)} {operator} {sp.latex(frac2)}'
                })
                steps.append({ 
                    'description': 'Kalikan pembilang dan penyebut',
                    'latex': f'\\frac{{{frac1.numerator} \\times {frac2.numerator}}}{{{frac1.denominator} \\times {frac2.denominator}}} = \\frac{{{frac1.numerator * frac2.numerator}}}{{{frac1.denominator * frac2.denominator}}}'
                })
                if sp.gcd(result.numerator, result.denominator) != 1: 
                    steps.append({ 
                        'description': 'Sederhanakan hasilnya',
                        'latex': f'\\frac{{{result.numerator} \\div {sp.gcd(result.numerator, result.denominator)}}}{{{result.denominator} \\div {sp.gcd(result.numerator, result.denominator)}}} = \\boxed{{{sp.latex(result)}}}'
                    })
                else:
                    steps.append({ 
                        'description': 'Hasil akhir (sudah disederhanakan)',
                        'latex': f'\\boxed{{{sp.latex(result)}}}'
                    })
            elif action == "divide": 
                operator = "\\div" 
                steps.append({ 
                    'description': 'Pecahan yang akan dibagi',
                    'latex': f'{sp.latex(frac1)} {operator} {sp.latex(frac2)}'
                })
                steps.append({ 
                    'description': 'Ubah pembagian menjadi perkalian dengan membalik pecahan kedua',
                    'latex': f'{sp.latex(frac1)} \\times \\frac{{{frac2.denominator}}}{{{frac2.numerator}}}'
                })
                steps.append({ 
                    'description': 'Kalikan pembilang dengan pembilang dan penyebut dengan penyebut',
                    'latex': f'\\frac{{{frac1.numerator} \\times {frac2.denominator}}}{{{frac1.denominator} \\times {frac2.numerator}}}'
                })
                steps.append({
                    'description': 'Hasil perkalian sebelum penyederhanaan',
                    'latex': f'= \\frac{{{frac1.numerator * frac2.denominator}}}{{{frac1.denominator * frac2.numerator}}}'
                })
                if sp.gcd(result.numerator, result.denominator) != 1: 
                    gcd = sp.gcd(result.numerator, result.denominator)
                    steps.append({ 
                        'description': 'Cari FPB dari pembilang dan penyebut untuk penyederhanaan',
                        'latex': f'\\text{{FPB dari }} {result.numerator} \\text{{ dan }} {result.denominator} = {gcd}'
                    })
                    steps.append({ 
                        'description': 'Sederhanakan dengan membagi pembilang dan penyebut dengan FPB',
                        'latex': f'\\frac{{{result.numerator} \\div {gcd}}}{{{result.denominator} \\div {gcd}}} = \\boxed{{{sp.latex(result)}}}'
                    })
                else:
                    steps.append({ 
                        'description': 'Hasil akhir (sudah disederhanakan)',
                        'latex': f'\\boxed{{{sp.latex(result)}}}'
                    })
            elif action == "compare": 
                steps.append({ 
                    'description': 'Bandingkan pecahan',
                    'latex': f'{sp.latex(frac1)} \\text{{ dan }} {sp.latex(frac2)}'
                })
                steps.append({ 
                    'description': 'Cari penyebut umum untuk perbandingan',
                    'latex': f'\\frac{{{frac1.numerator} \\times {frac2.denominator}}}{{{frac1.denominator} \\times {frac2.denominator}}} = \\frac{{{frac1.numerator * frac2.denominator}}}{{{frac1.denominator * frac2.denominator}}}'
                })
                steps.append({ 
                    'description': '',
                    'latex': f'\\frac{{{frac2.numerator} \\times {frac1.denominator}}}{{{frac2.denominator} \\times {frac1.denominator}}} = \\frac{{{frac2.numerator * frac1.denominator}}}{{{frac2.denominator * frac1.denominator}}}'
                })
                steps.append({ 
                    'description': 'Bandingkan pembilang',
                    'latex': f'{frac1.numerator * frac2.denominator} \\text{{ vs }} {frac2.numerator * frac1.denominator}'
                })
                steps.append({ 
                    'description': 'Hasil perbandingan',
                    'latex': f'\\boxed{{{result}}}'
                })
            elif action == "convert": 
                steps.append({ 
                    'description': 'Ubah pecahan ke desimal',
                    'latex': f'{sp.latex(frac1)} = {frac1.numerator} \\div {frac1.denominator}'
                })
                steps.append({ 
                    'description': 'Hasil pembagian',
                    'latex': f'= {float(frac1)}'
                })

        elif operation == 'aritmatika': 
            expr = sp.sympify(expression) 
            steps.append({ 
                'description': 'Evaluasi Ekspresi Aritmatika',
                'latex': f'\\text{{Diberikan: }} {sp.latex(expr)}'
            })
            
            if expr.is_Add: 
                terms = expr.args 
                current_sum = terms[0] 
                steps.append({ 
                    'description': 'Mulai dengan suku pertama',
                    'latex': f'= {sp.latex(current_sum)}'
                })
                for term in terms[1:]: 
                    steps.append({ 
                        'description': f'Tambahkan suku berikutnya: {sp.latex(term)}',
                        'latex': f'= {sp.latex(current_sum)} + {sp.latex(term)} = {sp.latex(current_sum + term)}'
                    })
                    current_sum += term 
            elif expr.is_Mul: 
                factors = expr.args 
                current_prod = factors[0] 
                steps.append({ 
                    'description': 'Mulai dengan faktor pertama',
                    'latex': f'= {sp.latex(current_prod)}'
                })
                for factor in factors[1:]: 
                    steps.append({ 
                        'description': f'Kalikan dengan faktor berikutnya: {sp.latex(factor)}',
                        'latex': f'= {sp.latex(current_prod)} \\times {sp.latex(factor)} = {sp.latex(current_prod * factor)}'
                    })
                    current_prod *= factor 
            elif expr.is_Pow: 
                base, exponent = expr.args 
                steps.append({ 
                    'description': 'Hitung pangkat',
                    'latex': f'= {sp.latex(base)}^{{{sp.latex(exponent)}}}'
                })
                if exponent.is_Integer: 
                    if exponent > 0: 
                        steps.append({ 
                            'description': f'Kalikan {base} dengan dirinya sendiri {exponent-1} kali',
                            'latex': f'= {sp.latex(base)}' + f' \\times {sp.latex(base)}'*(exponent-1)
                        })
                    elif exponent < 0: 
                        steps.append({ 
                            'description': 'Pangkat negatif berarti kebalikan',
                            'latex': f'= \\frac{{1}}{{{sp.latex(base)}^{{{-exponent}}}}}'
                        })
            
            steps.append({ 
                'description': 'Hasil akhir',
                'latex': f'\\boxed{{{sp.latex(result)}}}'
            })

        elif operation == 'turunan': 
            var = sp.Symbol(variables[0])
            expr = sp.sympify(expression)
            
            steps.append({
                'description': 'Memulai Perhitungan Turunan',
                'latex': f'\\text{{Fungsi yang diberikan: }} f({variables[0]}) = {sp.latex(expr)}'
            })
            steps.append({
                'description': 'Kita akan mencari turunan terhadap variabel',
                'latex': f'\\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(expr)}\\right]'
            })

            # Handle different types of expressions with more detail
            if expr.is_Add:
                steps.append({
                    'description': 'Fungsi terdiri dari penjumlahan beberapa suku',
                    'latex': f'= \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(expr.args[0])}\\right] + \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(expr.args[1])}\\right]' + 
                        (' + \\cdots' if len(expr.args) > 2 else '')
                })
                for i, term in enumerate(expr.args):
                    term_deriv = sp.diff(term, var)
                    steps.append({
                        'description': f'Menghitung turunan suku ke-{i+1}: {sp.latex(term)}',
                        'latex': f'\\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(term)}\\right] = {sp.latex(term_deriv)}'
                    })
                
            elif expr.is_Mul:
                steps.append({
                    'description': 'Fungsi terdiri dari perkalian beberapa faktor. Kita akan menggunakan aturan perkalian (uv)\' = u\'v + uv\'',
                    'latex': ''
                })
                
                # Handle multiplication with more than 2 factors
                if len(expr.args) > 2:
                    steps.append({
                        'description': 'Kelompokkan faktor-faktor untuk menerapkan aturan perkalian secara bertahap',
                        'latex': f'= \\frac{{d}}{{d{variables[0]}}}\\left[({sp.latex(expr.args[0])})({sp.latex(sp.Mul(*expr.args[1:]))})\\right]'
                    })
                    u = expr.args[0]
                    v = sp.Mul(*expr.args[1:])
                else:
                    u, v = expr.args[0], expr.args[1]
                
                steps.append({
                    'description': 'Terapkan aturan perkalian: (uv)\' = u\'v + uv\'',
                    'latex': f'= \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(u)}\\right] \\cdot {sp.latex(v)} + {sp.latex(u)} \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(v)}\\right]'
                })
                
                u_deriv = sp.diff(u, var)
                v_deriv = sp.diff(v, var)
                
                steps.append({
                    'description': 'Hitung turunan masing-masing bagian',
                    'latex': f'= {sp.latex(u_deriv)} \\cdot {sp.latex(v)} + {sp.latex(u)} \\cdot {sp.latex(v_deriv)}'
                })
                
                # If either derivative requires further expansion
                if any(arg.has(sp.Derivative) for arg in [u_deriv, v_deriv]):
                    steps.append({
                        'description': 'Perluas turunan yang lebih kompleks',
                        'latex': f'= {sp.latex(u_deriv * v + u * v_deriv)}'
                    })
                
            elif expr.is_Pow:
                base, exponent = expr.args
                steps.append({
                    'description': 'Fungsi berupa perpangkatan. Kita akan menggunakan aturan rantai untuk pangkat',
                    'latex': ''
                })
                
                if base == var:
                    steps.append({
                        'description': 'Kasus dasar: turunan dari x^n',
                        'latex': f'= {sp.latex(exponent)} \\cdot {variables[0]}^{{{sp.latex(exponent-1)}}}'
                    })
                else:
                    steps.append({
                        'description': 'Kasus umum: turunan dari [u(x)]^n menggunakan aturan rantai',
                        'latex': f'= {sp.latex(exponent)} \\cdot {sp.latex(base)}^{{{sp.latex(exponent-1)}}} \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(base)}\\right]'
                    })
                    base_deriv = sp.diff(base, var)
                    steps.append({
                        'description': 'Hitung turunan dari fungsi dasar',
                        'latex': f'= {sp.latex(exponent)} \\cdot {sp.latex(base)}^{{{sp.latex(exponent-1)}}} \\cdot {sp.latex(base_deriv)}'
                    })
            
            elif expr.is_Function:
                # Handle composite functions with detailed chain rule
                func_name = expr.func.__name__
                arg = expr.args[0]
                
                steps.append({
                    'description': f'Fungsi berupa {func_name}. Kita akan menggunakan aturan rantai',
                    'latex': ''
                })
                
                if func_name == 'sin':
                    steps.append({
                        'description': 'Turunan sin(u) adalah cos(u) dikali turunan u',
                        'latex': f'= \\cos({sp.latex(arg)}) \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(arg)}\\right]'
                    })
                elif func_name == 'cos':
                    steps.append({
                        'description': 'Turunan cos(u) adalah -sin(u) dikali turunan u',
                        'latex': f'= -\\sin({sp.latex(arg)}) \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(arg)}\\right]'
                    })
                elif func_name == 'tan':
                    steps.append({
                        'description': 'Turunan tan(u) adalah sec²(u) dikali turunan u',
                        'latex': f'= \\sec^2({sp.latex(arg)}) \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(arg)}\\right]'
                    })
                elif func_name == 'exp':
                    steps.append({
                        'description': 'Turunan e^u adalah e^u dikali turunan u',
                        'latex': f'= e^{{{sp.latex(arg)}}} \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(arg)}\\right]'
                    })
                elif func_name == 'log':
                    steps.append({
                        'description': 'Turunan ln(u) adalah 1/u dikali turunan u',
                        'latex': f'= \\frac{{1}}{{{sp.latex(arg)}}} \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(arg)}\\right]'
                    })
                
                arg_deriv = sp.diff(arg, var)
                steps.append({
                    'description': 'Hitung turunan dari argumen fungsi',
                    'latex': f'= {sp.latex(expr.func(arg).diff(var))}'
                })
            
            elif expr.is_Quotient:
                u, v = expr.as_numer_denom()
                steps.append({
                    'description': 'Fungsi berupa pecahan. Kita akan menggunakan aturan hasil bagi',
                    'latex': f'= \\frac{{\\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(u)}\\right] \\cdot {sp.latex(v)} - {sp.latex(u)} \\cdot \\frac{{d}}{{d{variables[0]}}}\\left[{sp.latex(v)}\\right]}}{{{sp.latex(v)}^2}}'
                })
                
                u_deriv = sp.diff(u, var)
                v_deriv = sp.diff(v, var)
                
                steps.append({
                    'description': 'Hitung turunan pembilang dan penyebut',
                    'latex': f'= \\frac{{{sp.latex(u_deriv)} \\cdot {sp.latex(v)} - {sp.latex(u)} \\cdot {sp.latex(v_deriv)}}}{{{sp.latex(v)}^2}}'
                })
                
                steps.append({
                    'description': 'Perluas dan sederhanakan hasilnya',
                    'latex': f'= {sp.latex((u_deriv * v - u * v_deriv) / (v**2))}'
                })
            
            steps.append({
                'description': 'Turunan akhir dari fungsi',
                'latex': f'f\'({variables[0]}) = \\boxed{{{sp.latex(result)}}}'
            })

        elif operation == 'integral':
            var = sp.Symbol(variables[0])
            expr = sp.sympify(expression)
            
            steps.append({
                'description': 'Memulai Perhitungan Integral Tak Tentu',
                'latex': f'\\text{{Fungsi yang diberikan: }} \\int {sp.latex(expr)} \\, d{variables[0]}'
            })
            
            # Handle different types of integrals with more detail
            if expr.is_Add:
                steps.append({
                    'description': 'Fungsi terdiri dari penjumlahan beberapa suku. Integral dapat dipecah menjadi penjumlahan integral',
                    'latex': f'= \\int {sp.latex(expr.args[0])} \\, d{variables[0]} + \\int {sp.latex(expr.args[1])} \\, d{variables[0]}' + 
                             (' + \\cdots' if len(expr.args) > 2 else '') + ' + C'
                })
                for i, term in enumerate(expr.args):
                    term_integral = sp.integrate(term, var)
                    steps.append({
                        'description': f'Hitung integral suku ke-{i+1}: {sp.latex(term)}',
                        'latex': f'\\int {sp.latex(term)} \\, d{variables[0]} = {sp.latex(term_integral)} + C_{i+1}'
                    })
                
                steps.append({
                    'description': 'Gabungkan semua hasil integral dan konstanta',
                    'latex': f'= {sp.latex(result)} + C \\quad (\\text{{dimana }} C = C_1 + C_2 + \\cdots)'
                })
            
            elif expr.is_Pow:
                base, exponent = expr.args
                if base == var:
                    if exponent == -1:
                        steps.append({
                            'description': 'Kasus khusus integral 1/x',
                            'latex': f'= \\ln|{variables[0]}| + C'
                        })
                    else:
                        steps.append({
                            'description': 'Gunakan aturan pangkat untuk integral',
                            'latex': f'= \\frac{{{variables[0]}^{{{sp.latex(exponent+1)}}}}}{{{{sp.latex(exponent+1)}}}} + C \\quad (\\text{{untuk }} n \\neq -1)'                        })
                else:
                    steps.append({
                        'description': 'Integral fungsi pangkat yang lebih kompleks mungkin memerlukan substitusi',
                        'latex': f'\\text{{Pertimbangkan substitusi }} u = {sp.latex(base)} \\text{{ dan }} du = {sp.latex(sp.diff(base, var))} d{variables[0]}'
                    })
            
            elif expr.is_Function:
                func_name = expr.func.__name__
                arg = expr.args[0]
                
                steps.append({
                    'description': f'Integral fungsi {func_name} mungkin memerlukan teknik khusus',
                    'latex': ''
                })
                
                if func_name == 'sin':
                    if arg == var:
                        steps.append({
                            'description': 'Integral langsung dari sin(x)',
                            'latex': f'= -\\cos({variables[0]}) + C'
                        })
                    else:
                        steps.append({
                            'description': 'Gunakan substitusi untuk integral sin(u)',
                            'latex': f'\\text{{Misalkan }} u = {sp.latex(arg)}, \\quad du = {sp.latex(sp.diff(arg, var))} d{variables[0]}'
                        })
                        steps.append({
                            'description': 'Ubah integral ke dalam bentuk u',
                            'latex': f'= \\int \\sin(u) \\frac{{du}}{{{sp.latex(sp.diff(arg, var))}}}'
                        })
                        steps.append({
                            'description': 'Integralkan terhadap u',
                            'latex': f'= -\\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} \\cos(u) + C'
                        })
                        steps.append({
                            'description': 'Substitusi kembali u',
                            'latex': f'= -\\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} \\cos({sp.latex(arg)}) + C'
                        })
                
                elif func_name == 'cos':
                    if arg == var:
                        steps.append({
                            'description': 'Integral langsung dari cos(x)',
                            'latex': f'= \\sin({variables[0]}) + C'
                        })
                    else:
                        steps.append({
                            'description': 'Gunakan substitusi untuk integral cos(u)',
                            'latex': f'\\text{{Misalkan }} u = {sp.latex(arg)}, \\quad du = {sp.latex(sp.diff(arg, var))} d{variables[0]}'
                        })
                        steps.append({
                            'description': 'Ubah integral ke dalam bentuk u',
                            'latex': f'= \\int \\cos(u) \\frac{{du}}{{{sp.latex(sp.diff(arg, var))}}}'
                        })
                        steps.append({
                            'description': 'Integralkan terhadap u',
                            'latex': f'= \\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} \\sin(u) + C'
                        })
                        steps.append({
                            'description': 'Substitusi kembali u',
                            'latex': f'= \\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} \\sin({sp.latex(arg)}) + C'
                        })
                
                elif func_name == 'exp':
                    if arg == var:
                        steps.append({
                            'description': 'Integral langsung dari e^x',
                            'latex': f'= e^{{{variables[0]}}} + C'
                        })
                    else:
                        steps.append({
                            'description': 'Gunakan substitusi untuk integral e^u',
                            'latex': f'\\text{{Misalkan }} u = {sp.latex(arg)}, \\quad du = {sp.latex(sp.diff(arg, var))} d{variables[0]}'
                        })
                        steps.append({
                            'description': 'Ubah integral ke dalam bentuk u',
                            'latex': f'= \\int e^u \\frac{{du}}{{{sp.latex(sp.diff(arg, var))}}}'
                        })
                        steps.append({
                            'description': 'Integralkan terhadap u',
                            'latex': f'= \\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} e^u + C'
                        })
                        steps.append({
                            'description': 'Substitusi kembali u',
                            'latex': f'= \\frac{{1}}{{{sp.latex(sp.diff(arg, var))}}} e^{{{sp.latex(arg)}}} + C'
                        })
            
            elif expr.is_Quotient:
                u, v = expr.as_numer_denom()
                steps.append({
                    'description': 'Integral pecahan mungkin memerlukan teknik khusus seperti dekomposisi pecahan parsial atau substitusi',
                    'latex': f'\\text{{Perhatikan integral }} \\int \\frac{{{sp.latex(u)}}}{{{sp.latex(v)}}} \\, d{variables[0]}'
                })
                
                # Check for simple cases like u = v'
                v_deriv = sp.diff(v, var)
                if u == v_deriv:
                    steps.append({
                        'description': 'Kasus khusus: pembilang adalah turunan penyebut',
                        'latex': f'= \\ln|{sp.latex(v)}| + C'
                    })
                else:
                    steps.append({
                        'description': 'Teknik yang lebih canggih mungkin diperlukan untuk integral ini',
                        'latex': f'\\text{{Pertimbangkan substitusi atau dekomposisi pecahan parsial}}'
                    })
            
            steps.append({
                'description': 'Hasil integral akhir',
                'latex': f'\\int {sp.latex(expr)} \\, d{variables[0]} = \\boxed{{{sp.latex(result)} + C}}'
            })

        elif operation == 'integral_tentu':
            var = sp.Symbol(variables[0])
            expr = sp.sympify(expression)
            a = sp.sympify(params.get("lower_bound", 0))
            b = sp.sympify(params.get("upper_bound", 1))
            
            steps.append({
                'description': 'Memulai Perhitungan Integral Tentu',
                'latex': f'\\text{{Fungsi yang diberikan: }} \\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(expr)} \\, d{variables[0]}'
            })
            
            # First find the indefinite integral
            antiderivative = sp.integrate(expr, var)
            steps.append({
                'description': 'Langkah 1: Cari antiturunan (integral tak tentu)',
                'latex': f'F({variables[0]}) = \\int {sp.latex(expr)} \\, d{variables[0]} = {sp.latex(antiderivative)} + C'
            })
            
            steps.append({
                'description': 'Langkah 2: Terapkan Teorema Dasar Kalkulus',
                'latex': f'= F({sp.latex(b)}) - F({sp.latex(a)})'
            })
            
            # Evaluate at upper bound
            upper_val = antiderivative.subs(var, b)
            steps.append({
                'description': 'Langkah 3: Evaluasi antiturunan pada batas atas',
                'latex': f'F({sp.latex(b)}) = {sp.latex(antiderivative.subs(var, b))} = {sp.latex(upper_val)}'
            })
            
            # Evaluate at lower bound
            lower_val = antiderivative.subs(var, a)
            steps.append({
                'description': 'Langkah 4: Evaluasi antiturunan pada batas bawah',
                'latex': f'F({sp.latex(a)}) = {sp.latex(antiderivative.subs(var, a))} = {sp.latex(lower_val)}'
            })
            
            steps.append({
                'description': 'Langkah 5: Hitung selisih nilai pada batas atas dan bawah',
                'latex': f'= {sp.latex(upper_val)} - ({sp.latex(lower_val)})'
            })
            
            steps.append({
                'description': 'Hasil integral tentu',
                'latex': f'\\int_{{{sp.latex(a)}}}^{{{sp.latex(b)}}} {sp.latex(expr)} \\, d{variables[0]} = \\boxed{{{sp.latex(result)}}}'
            })

            # Handle special cases with substitution
            if expr.has(sp.sin) or expr.has(sp.cos):
                func = sp.sin if expr.has(sp.sin) else sp.cos
                arg = expr.args[0]
                
                if arg != var and arg.is_Mul:  # Check if argument is a*var
                    coeff, inner_var = arg.as_coeff_Mul()
                    if inner_var == var:
                        steps.insert(1, {
                            'description': 'Metode Alternatif: Substitusi',
                            'latex': f'\\text{{Kita dapat menggunakan substitusi untuk menyelesaikan integral ini}}'
                        })
                        steps.insert(2, {
                            'description': f'Substitusi: u = {sp.latex(arg)}',
                            'latex': f'\\text{{Misalkan }} u = {sp.latex(arg)}, \\quad du = {sp.latex(coeff)} \\, d{variables[0]}'
                        })
                        steps.insert(3, {
                            'description': 'Ubah batas integral sesuai substitusi',
                            'latex': f'\\text{{Ketika }} {variables[0]} = {sp.latex(a)}, \\quad u = {sp.latex(coeff * a)}; \\quad \\text{{Ketika }} {variables[0]} = {sp.latex(b)}, \\quad u = {sp.latex(coeff * b)}'
                        })
                        steps.insert(4, {
                            'description': 'Ubah integral ke dalam bentuk u',
                            'latex': f'= \\frac{{1}}{{{sp.latex(coeff)}}} \\int_{{{sp.latex(coeff * a)}}}^{{{sp.latex(coeff * b)}}} {sp.latex(func(sp.Symbol("u")))} \\, du'
                        })
                        antiderivative_u = -sp.cos(sp.Symbol("u")) if func == sp.sin else sp.sin(sp.Symbol("u"))
                        steps.insert(5, {
                            'description': f'Integralkan: \\int {sp.latex(func(sp.Symbol("u")))} du = {sp.latex(antiderivative_u)}',
                            'latex': f'= \\frac{{1}}{{{sp.latex(coeff)}}} \\left[{sp.latex(antiderivative_u)}\\right]_{{{sp.latex(coeff * a)}}}^{{{sp.latex(coeff * b)}}}'
                        })
                        upper_val_u = antiderivative_u.subs(sp.Symbol("u"), coeff * b)
                        lower_val_u = antiderivative_u.subs(sp.Symbol("u"), coeff * a)
                        steps.insert(6, {
                            'description': 'Evaluasi pada batas atas dan bawah',
                            'latex': f'= \\frac{{1}}{{{sp.latex(coeff)}}} \\left({sp.latex(upper_val_u)} - ({sp.latex(lower_val_u)})\\right)'
                        })
                        steps.insert(7, {
                            'description': 'Sederhanakan hasil',
                            'latex': f'= \\boxed{{{sp.latex(result)}}}'
                        })


        elif operation == 'persamaan': 
            if isinstance(result, list): 
                eq_expr = sp.sympify(expression.split('=')[0]) - sp.sympify(expression.split('=')[1]) if '=' in expression else sp.sympify(expression) 
                steps.append({ 
                    'description': 'Selesaikan Persamaan',
                    'latex': f'\\text{{Diberikan: }} {expression.replace("=", " = ")}'
                })
                
                steps.append({ 
                    'description': 'Tulis ulang persamaan dalam bentuk standar',
                    'latex': f'{sp.latex(eq_expr)} = 0'
                })
                
                if eq_expr.is_Add: 
                    const_term = 0 
                    var_term = eq_expr 
                    for term in eq_expr.args: 
                        if term.is_constant(): 
                            const_term += term 
                            var_term -= term 
                    steps.append({ 
                        'description': 'Pindahkan suku konstanta ke sisi lain',
                        'latex': f'{sp.latex(var_term)} = {sp.latex(-const_term)}'
                    })
                    if var_term.is_Mul: 
                        coeff = var_term.args[0] 
                        var_part = var_term.args[1] 
                        steps.append({ 
                            'description': 'Bagi kedua sisi dengan koefisien',
                            'latex': f'{sp.latex(var_part)} = \\frac{{{sp.latex(-const_term)}}}{{{sp.latex(coeff)}}}'
                        })
                        steps.append({ 
                            'description': 'Sederhanakan',
                            'latex': f'{variables[0]} = {sp.latex(result[0])}'
                        })
                
                if len(result) == 1: 
                    steps.append({ 
                        'description': 'Satu solusi ditemukan',
                        'latex': f'{variables[0]} = \\boxed{{{sp.latex(result[0])}}}'
                    })
                else:
                    solutions = ', '.join([f'{variables[0]} = {sp.latex(sol)}' for sol in result]) 
                    steps.append({ 
                        'description': f'Ditemukan {len(result)} solusi',
                        'latex': f'\\boxed{{{solutions}}}'
                    })

        elif operation == 'faktorisasi' or operation == 'factor': 
            expr = sp.sympify(expression) 
            steps.append({ 
                'description': 'Faktorkan Ekspresi',
                'latex': f'\\text{{Diberikan: }} {sp.latex(expr)}'
            })
            
            if expr.is_Add: 
                common_factor = sp.gcd_terms(expr) 
                if common_factor != 1: 
                    steps.append({ 
                        'description': 'Cari faktor persekutuan terbesar',
                        'latex': f'\\text{{FPB: }} {sp.latex(common_factor)}'
                    })
                    factored = sp.factor(expr) 
                    steps.append({ 
                        'description': 'Faktorkan FPB',
                        'latex': f'= {sp.latex(common_factor)} \\cdot \\left({sp.latex(factored/common_factor)}\\right)'
                    })
            elif expr.is_Pow: 
                base, exp = expr.args 
                if base.is_Add and exp == 2: 
                    steps.append({ 
                        'description': 'Kenali kuadrat sempurna',
                        'latex': f'= ({sp.latex(sp.sqrt(base))})^2'
                    })
            
            steps.append({ 
                'description': 'Bentuk faktor akhir',
                'latex': f'{sp.latex(expr)} = \\boxed{{{sp.latex(result)}}}'
            })

        elif operation == 'limit': 
            var = sp.Symbol(variables[0]) 
            expr = sp.sympify(expression) 
            point = params.get("point", 0) 
            
            steps.append({ 
                'description': 'Hitung Limit',
                'latex': f'\\lim_{{{variables[0]} \\to {sp.latex(sp.sympify(point))}}} {sp.latex(expr)}'
            })
            
            try:
                direct_sub = expr.subs(var, point) 
                if direct_sub.is_finite: 
                    steps.append({ 
                        'description': 'Substitusi langsung',
                        'latex': f'= {sp.latex(direct_sub)}'
                    })
                else:
                    steps.append({ 
                        'description': 'Substitusi langsung menghasilkan bentuk tak tentu',
                        'latex': f'\\text{{Mensubstitusikan }} {variables[0]} = {point} \\text{{ menghasilkan }} {sp.latex(direct_sub)}'
                    })
                    if sp.limit(expr, var, point, dir='-') == sp.limit(expr, var, point, dir='+'): 
                        steps.append({ 
                            'description': 'Limit kiri dan kanan sama',
                            'latex': f'\\lim_{{{variables[0]} \\to {point}^-}} = \\lim_{{{variables[0]} \\to {point}^+}} = {sp.latex(result)}'
                        })
                    else:
                        steps.append({ 
                            'description': 'Limit kiri dan kanan berbeda',
                            'latex': f'\\text{{Limit tidak ada (limit kiri ≠ limit kanan)}}'
                        })
            except:
                steps.append({ 
                    'description': 'Mengevaluasi limit memerlukan teknik khusus',
                    'latex': f'\\text{{Menggunakan properti limit dan manipulasi aljabar}}'
                })
            
            steps.append({ 
                'description': 'Nilai limit akhir',
                'latex': f'\\lim_{{{variables[0]} \\to {sp.latex(sp.sympify(point))}}} {sp.latex(expr)} = \\boxed{{{sp.latex(result)}}}'
            })

        elif operation == 'deret_aritmatika': 
            first_term = params.get("first_term", 1) 
            common_diff = params.get("common_diff", 1) 
            n_term = params.get("n_term", 1) 
            seq_type = params.get("seq_type", "term") 
            
            steps.append({ 
                'description': 'Barisan Aritmatika',
                'latex': f'\\text{{Diberikan: }} a_1 = {first_term}, \\quad d = {common_diff}'
            })
            
            if seq_type == "term": 
                steps.append({ 
                    'description': 'Rumus suku ke-n barisan aritmatika',
                    'latex': f'a_n = a_1 + (n-1) \\cdot d'
                })
                steps.append({ 
                    'description': f'Substitusikan untuk mencari suku ke-{n_term}',
                    'latex': f'a_{{{n_term}}} = {first_term} + ({n_term}-1) \\cdot {common_diff}'
                })
                steps.append({ 
                    'description': 'Hitung',
                    'latex': f'= {first_term} + {n_term-1} \\times {common_diff}'
                })
                steps.append({ 
                    'description': 'Nilai suku akhir',
                    'latex': f'= \\boxed{{{result}}}'
                })
            else:
                steps.append({ 
                    'description': 'Rumus jumlah n suku pertama barisan aritmatika',
                    'latex': f'S_n = \\frac{{n}}{{2}}[2a_1 + (n-1)d]'
                })
                steps.append({ 
                    'description': f'Substitusikan untuk mencari jumlah {n_term} suku pertama',
                    'latex': f'S_{{{n_term}}} = \\frac{{{n_term}}}{{2}}[2 \\times {first_term} + ({n_term}-1) \\times {common_diff}]'
                })
                steps.append({ 
                    'description': 'Hitung suku di dalam kurung',
                    'latex': f'= \\frac{{{n_term}}}{{2}}[{2*first_term} + {(n_term-1)*common_diff}]'
                })
                steps.append({ 
                    'description': 'Kalikan',
                    'latex': f'= \\frac{{{n_term}}}{{2}} \\times {2*first_term + (n_term-1)*common_diff}'
                })
                steps.append({ 
                    'description': 'Jumlah akhir',
                    'latex': f'= \\boxed{{{result}}}'
                })

        elif operation == 'deret_geometri': 
            first_term = params.get("first_term", 1) 
            common_ratio = params.get("common_ratio", 2) 
            n_term = params.get("n_term", 1) 
            seq_type = params.get("seq_type", "term") 
            
            steps.append({ 
                'description': 'Barisan Geometri',
                'latex': f'\\text{{Diberikan: }} a_1 = {first_term}, \\quad r = {common_ratio}'
            })
            
            if seq_type == "term": 
                steps.append({ 
                    'description': 'Rumus suku ke-n barisan geometri',
                    'latex': f'a_n = a_1 \\cdot r^{{n-1}}'
                })
                steps.append({ 
                    'description': f'Substitusikan untuk mencari suku ke-{n_term}',
                    'latex': f'a_{{{n_term}}} = {first_term} \\times {common_ratio}^{{{n_term}-1}}'
                })
                steps.append({ 
                    'description': 'Hitung eksponen',
                    'latex': f'= {first_term} \\times {common_ratio**(n_term-1)}'
                })
                steps.append({ 
                    'description': 'Nilai suku akhir',
                    'latex': f'= \\boxed{{{result}}}'
                })
            else:
                if common_ratio != 1: 
                    steps.append({ 
                        'description': 'Rumus jumlah n suku pertama barisan geometri (r ≠ 1)',
                        'latex': f'S_n = a_1 \\cdot \\frac{{r^n - 1}}{{r - 1}}'
                    })
                    steps.append({ 
                        'description': f'Substitusikan untuk mencari jumlah {n_term} suku pertama',
                        'latex': f'S_{{{n_term}}} = {first_term} \\times \\frac{{{common_ratio}^{{{n_term}}} - 1}}{{{common_ratio} - 1}}'
                    })
                    steps.append({ 
                        'description': 'Hitung pembilang dan penyebut',
                        'latex': f'= {first_term} \\times \\frac{{{common_ratio**n_term} - 1}}{{{common_ratio - 1}}}'
                    })
                    steps.append({ 
                        'description': 'Jumlah akhir',
                        'latex': f'= \\boxed{{{result}}}'
                    })
                else:
                    steps.append({ 
                        'description': 'Kasus khusus ketika rasio umum adalah 1',
                        'latex': f'S_n = n \\times a_1'
                    })
                    steps.append({ 
                        'description': 'Hitung jumlah',
                        'latex': f'S_{{{n_term}}} = {n_term} \\times {first_term}'
                    })
                    steps.append({ 
                        'description': 'Jumlah akhir',
                        'latex': f'= \\boxed{{{result}}}'
                    })

        else:
            expr = sp.sympify(expression) if expression else None 
            if expr: 
                steps.append({ 
                    'description': f'Operasi: {operation.title()}',
                    'latex': f'\\text{{Masukan: }} {sp.latex(expr)}'
                })
                if operation == 'simplify': 
                    steps.append({ 
                        'description': 'Terapkan aturan penyederhanaan',
                        'latex': f'\\text{{Bentuk sederhana: }} {sp.latex(result)}'
                    })
                elif operation == 'expand': 
                    steps.append({ 
                        'description': 'Terapkan aturan perluasan',
                        'latex': f'\\text{{Bentuk diperluas: }} {sp.latex(result)}'
                    })
                steps.append({ 
                    'description': 'Hasil akhir',
                    'latex': f'\\boxed{{{sp.latex(result)}}}'
                })

    except Exception as e:
        steps = [{ 
            'description': 'Terjadi kesalahan dalam menghasilkan langkah-langkah LaTeX',
            'latex': f'\\text{{Hasil: }} {str(result)}'
        }]
    
    return steps 