FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["SDR.Core.API.csproj", "./"]
RUN dotnet restore "SDR.Core.API.csproj"
COPY . .
RUN dotnet build "SDR.Core.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "SDR.Core.API.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "SDR.Core.API.dll"]
