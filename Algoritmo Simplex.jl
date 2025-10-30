using LinearAlgebra

function main()
    m = 0
    n = 0

    while m <= 0 || n <= 0
        if m <= 0
            m = pedirM()
        end

        if n <= 0
            n = pedirN()
        end

        if m <= 0 || n <= 0
            println("M e N devem ser maiores que 0, por favor corrija os dados.")
            println("")
        end
    end
    
    c = zeros(Float64, n)
    b = zeros(Float64, m)
    A = zeros(Float64, m, n)

    c = receberCustos(n)
    println("vetor de custos: ", c)

    b = receberRecursos(m)
    println("vetor de recursos: ", b)

    A = receberCoeficientes(m, n)
    println("Matriz dos coeficientes: ",A)

    calculoComY(A, b, c)
end

function pedirM()
    print("Número de restrições (linhas) do seu sistema: ")
    return parse(Int128, readline())
end

function pedirN()
    println("")
    print("Número de variáveis (colunas) do seu sistema: ")
    return parse(Int128, readline())
end

function receberCustos(n)
    custos = zeros(Float64, n)
    println("")
    print("Digite os coeficientes de custo (c) associados às variáveis: ")
    linha = split(readline())

    while size(linha, 1) != n
        println("")
        println("É necessário inserir ", n, " coeficientes de custos.")
        print("Insira novamente os coeficientes: ")
        linha = split(readline())
    end

    for j in 1:n
        if occursin("/", linha[j])
            fracao = parse.(Float64, split(linha[j], "/"))
            custos[j] = fracao[1]/fracao[2]
        else            
            custos[j] = parse(Float64, linha[j]) 
        end
    end  
    return custos
end

function receberRecursos(m)
    recursos = zeros(Float64, m)
    println("")
    print("Digite os coeficientes de recurso (b): ")
    linha = split(readline())

    while size(linha, 1) != m
        println("")
        println("É necessário inserir ", m, " coeficientes de recursos.")
        print("Insira novamente os coeficientes: ")
        linha = split(readline())
    end

    for j in 1:m
        if occursin("/", linha[j])
            fracao = parse.(Float64, split(linha[j], "/"))
            recursos[j] = fracao[1]/fracao[2]
        else            
            recursos[j] = parse(Float64, linha[j]) 
        end
    end
    return recursos
end

function receberCoeficientes(m, n)
    println("")
    coeficientes = zeros(Float64, m, n )
    for j in 1:m
        print("Digite a linha ", j, " do seu sistema: ")
        linha = split(readline())

        while size(linha, 1) != n
            println("")
            println("É preciso inserir exatamente ", n, " coeficientes por linha.")
            print("Insira novamente os coeficientes: ")
            linha = split(readline())
        end

        for k in 1:n
            if occursin("/", linha[k])
                fracao = parse.(Float64, split(linha[k], "/"))
                coeficientes[j, k] = fracao[1]/fracao[2]
            else            
                coeficientes[j, k] = parse(Float64, linha[k]) 
            end
        end
    end
    return coeficientes
end

function calculoComY(A, b, c)
    m, n = size(A)
    identidade = Matrix{Float64}(I, m, m)
  
    Y = hcat(A, identidade)
    println("")
    println("Matriz com y's: ", Y)
    
    cb = ones(m)
    cn = zeros(n)
    cy = vcat(cn, cb)
    println("")
    println("custos com y: ", cy)

    B = deepcopy(identidade)
    N = deepcopy(A)
    println("")
    println("Colunas base: ", B)
    println("Colunas não-base: ", N)

    IB = zeros(Int128, m)
    IN = zeros(Int128, n)

    qtdn = 1
    qtdb = 1
    for i=1:(n+m)
        if cy[i] == 0
            IN[qtdn] = i
            qtdn+=1
        elseif cy[i] == 1
            IB[qtdb] = i
            qtdb+=1
        end
    end

    println("")
    println("Indices base: $([string(IB[k]) for k in 1:length(IB)])")
    println("Indices não-base : $([string(IN[k]) for k in 1:length(IN)])")

    refazer = true
    iteracoes = 1
    while refazer
        println(repeat("-", 80))
        println("ITERAÇÃO ", iteracoes, " com variáveis artificiais.")
        println(repeat("-", 80))

        xb = B \ b
        println("xb: ", xb)
    
        if !all(xb .≥ 0)
            println("Como xb tem índices negativos, o problema é infactível!")
            break
        elseif minimum(xb) == 0
            println("")
            println("Tem índice igual a zero, solução degenerada!")
        end

        f = cb'*xb
        println("Valor da função atual: ", f)

        λ = B' \ cb
        println("")
        println("Multiplicador simplex: ", λ)

        cnn = zeros(n)

        for i=1:n
            cnn[i] = cn[i] - λ'*N[:, i]
        end
        println("Custos relativos: ", cnn)

        minCn, indexEntra = findmin(cnn)
        if minCn ≥ 0
            if f != 0
                println("")
                println("O custo mínimo é ", minCn, ", que é ≥ 0.")
                println("Valor atual da função: ", f, ", é ≠ 0.")
                println("Logo o problema original é infactível.")
                break
            end
            println("O custo mínimo é ", minCn, ", que é ≥ 0.")
            println("Valor atual da função é = ", f)
            println("")
            println("Estamos na solução ótima!")
            println("O problema original é factível!")
            println("")
            println("Vetor xb: ", xb)
            println("")
            println("Base a ser utilizada: ", B)
            println("Não base: ", N)
            simplex(A, B, N, b, c, cb, cn, IB, IN)
            break
        end
        println("Custo mínimo: ", minCn, ". Coluna que entrará na base: ", IN[indexEntra])

        y = B \ N[:, indexEntra]
        println("")
        println("Direção simplex: ", y)

        if all(y .≤ 0)
            error("Y não possui valores > 0. Portanto não temos solução ótima finita.")
        end

        ϵ = zeros(m)

        for i=1:m
            if y[i] > 0
                ϵ[i] = xb[i]/y[i]
            else
                ϵ[i] = prevfloat(typemax(Float64))
            end
        end
        minϵ, indexSai = findmin(ϵ)

        println("Valor mínimo: ", minϵ, ". Coluna que sairá da base: ", IB[indexSai])

        aux = B[:, indexSai]
        B[:, indexSai] = N[:, indexEntra]
        N[:, indexEntra] = aux

        auxI = IB[indexSai]
        IB[indexSai] = IN[indexEntra]
        IN[indexEntra] = auxI

        auxC = cb[indexSai]
        cb[indexSai] = cn[indexEntra]
        cn[indexEntra] = auxC

        println("")
        println("Base após ", iteracoes, " iterações:", B)
        println("Não-base após ", iteracoes, " iterações:", N)
        
        println("")
        println("Indices base: $([string(IB[k]) for k in 1:length(IB)]) após $(iteracoes) iterações")
        println("Indices não-base: $([string(IN[k]) for k in 1:length(IN)]) após $(iteracoes) iterações")

        println("")
        println("Custos base: ", cb, " após ", iteracoes, " iterações")
        println("Custos não-base: ", cn, " após ", iteracoes, " iterações")

        iteracoes += 1
    end
end

function simplex(A, B, N, b, c, cb, cn, IB, IN)
    if any(x > size(A, 2) for x in IB)

    else
        m, n = size(A)
        refazer = true

        

        IN = sort([k for k in IN if k <= n])
        N = [A[:, k] for k in IN]
        cb = c[IB]
        cn = c[IN]

        iteracoes = 1
        while refazer
            println(repeat("-", 80))
            println("ITERAÇÃO ", iteracoes, " pós variáveis artificiais.")
            println(repeat("-", 80))

            xb = B \ b
            println("xb: ", xb)
    
            if !all(xb .≥ 0)
                error("Como xb tem indíces negativos é infactível!")
            elseif minimum(xb) == 0
                println("")
                println("Tem índice igual a zero, solução degenerada!")
            end
    
            f = cb'*xb
            println("Valor da função atual: ", f)
    
            λ = B' \ cb
            println("")
            println("Multiplicador simplex: ", λ)

            cnn = zeros(length(IN))

            for i=1:length(IN)
                cnn[i] = cn[i] - λ'*A[:,IN[i]]
            end
            println("Custos relativos: ", cnn)

            minCn, indexEntra = findmin(cnn)

            if minCn ≥ 0
                println("Custo mínimo: ", minCn, " ≥ 0.")

                respIB = ["X$(IB[k])" for k in 1:length(IB)]
                respIN = ["X$(IN[k])" for k in 1:length(IN)]

                if any(x == 0 for x in cnn)
                    println("")
                    println("O problema possui infinitas soluções ótimas.")
                    println("Uma delas é: Xb = ", respIB, " = ", xb, " e  Xn = ", respIN, " = ", [0 for k in 1:length(IN)])
                    println("Valor ótimo da função: ", f)
                    break
                else

                    println("")
                    println("Estamos na solução ótima!")
                    println("Solução: Xb = ", respIB, " = ", xb, " e Xn = ", respIN, " = ", [0 for k in 1:length(IN)])
                    println("Valor ótimo da função: ", f)
                    break
                end
            end
            println("Custo mínimo: ", minCn, ". Coluna que entrará na base: ", IN[indexEntra])

            y = B \ N[indexEntra]


            if all(y .≤ 0)
                println("")
                println("Y não tem valores > 0.")
                println("Problema não tem solução ótima finita!")
                break    
            end

            ϵ = zeros(Float64, length(y))
            for i=1:length(y)
                if y[i] > 0
                    ϵ[i] = xb[i]/y[i]
                else
                    ϵ[i] = prevfloat(typemax(Float64))
                end
            end
            minϵ, indexSai = findmin(ϵ)
            println("Valor mínimo: ", minϵ, ". Coluna que sairá da base: ", IB[indexSai])

            aux = B[:, indexSai]
            B[:, indexSai] = N[:, indexEntra]
            N[:, indexEntra] = aux
            
            auxI = IB[indexSai]
            IB[indexSai] = IN[indexEntra]
            IN[indexEntra] = auxI
            
            auxC = cb[indexSai]
            cb[indexSai] = cn[indexEntra]
            cn[indexEntra] = auxC
            
            println("")
            println("Base após ", iteracoes, " iterações:", B)
            println("Não-base após ", iteracoes, " iterações:", N)
            
            println("")
            println("Indices base: $([string(IB[k]) for k in 1:length(IB)]) após $(iteracoes) iterações")
            println("Indices não-base: $([string(IN[k]) for k in 1:length(IN)]) após $(iteracoes) iterações")

            println("")
            println("Custos base: ", cb, " após ", iteracoes, " iterações")
            println("Custos não-base: ", cn, " após ", iteracoes, " iterações")

            iteracoes += 1
        end
    end
end

main()