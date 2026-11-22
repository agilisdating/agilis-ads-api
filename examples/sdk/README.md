# SDK examples

The request example for every endpoint in the [API reference](https://www.agilis.dating/api-doc), for each official SDK. They are generated from the reference, one description per endpoint, so the code here is exactly what the reference shows. Please don't edit them by hand.

| Language | SDK | Folder |
|---|---|---|
| Node.js and TypeScript | [agilis-ads-node](https://github.com/agilisdating/agilis-ads-node) | [node](node) |
| Python | [agilis-ads-python](https://github.com/agilisdating/agilis-ads-python) | [python](python) |
| PHP | [agilis-ads-php](https://github.com/agilisdating/agilis-ads-php) | [php](php) |
| .NET (C#) | [agilis-ads-dotnet](https://github.com/agilisdating/agilis-ads-dotnet) | [dotnet](dotnet) |
| Java | [agilis-ads-java](https://github.com/agilisdating/agilis-ads-java) | [java](java) |
| Go | [agilis-ads-go](https://github.com/agilisdating/agilis-ads-go) | [go](go) |
| Ruby | [agilis-ads-ruby](https://github.com/agilisdating/agilis-ads-ruby) | [ruby](ruby) |

Each example reads your API key from `AGILIS_API_KEY`, makes one request and prints one field of the response. The C# and Java examples are shown in the reference as statements; here each is wrapped in a class so it compiles.

The [SDK examples workflow](../../.github/workflows/sdk-examples.yml) installs each SDK from its GitHub repository and checks that every example compiles against it:

| Language | Check |
|---|---|
| Node.js | `tsc --noEmit` in strict mode |
| Python | `mypy --strict` |
| PHP | `php -l` and PHPStan (level 8) |
| C# | `dotnet build`, with warnings as errors |
| Java | `javac` |
| Go | `gofmt`, `go vet` and `go build` |
| Ruby | `ruby -c`, and every SDK method an example calls exists |

The examples make real requests when run. Use a Test key (`pk_test_...`): Test Offers and Events are never shown to members and nothing is charged. Several examples use sample ids and file paths, such as `/path/to/offer.jpg`, which you replace with your own.
